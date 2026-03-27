import re
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


TOKEN_SPEC = [
    ("opsuma", r"[+\-]"),
    ("opmul",  r"[*/]"),
    ("pari",   r"\("),
    ("pard",   r"\)"),
    ("num",    r"[0-9]+"),
    ("id",     r"[a-zA-Z][0-9a-zA-Z]*"),
    ("WS",     r"[ \t]+"),
]

TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC))


def tokenizar(texto):
    tokens = []
    for m in TOKEN_RE.finditer(texto):
        tipo = m.lastgroup
        valor = m.group()
        if tipo != "WS":
            tokens.append((tipo, valor))
    return tokens


class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.hijos = []

    def agregar(self, hijo):
        self.hijos.append(hijo)
        return hijo


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None)

    def consumir(self, tipo):
        tok = self.actual()
        if tok[0] == tipo:
            self.pos += 1
            return tok
        return None

    def parse_E(self, nodo_padre):
        nodo = nodo_padre.agregar(Nodo("E"))
        pos_respaldo = self.pos
        if self.parse_T(nodo) and self.parse_Ep(nodo):
            return True
        self.pos = pos_respaldo
        nodo_padre.hijos.remove(nodo)
        return False

    def parse_Ep(self, nodo_padre):
        nodo = nodo_padre.agregar(Nodo("E'"))
        pos_respaldo = self.pos
        tok = self.consumir("opsuma")
        if tok:
            nodo.agregar(Nodo(f"opsuma({tok[1]})"))
            if self.parse_T(nodo) and self.parse_Ep(nodo):
                return True
            self.pos = pos_respaldo
            nodo_padre.hijos.remove(nodo)
            nodo_padre.agregar(Nodo("E'")).agregar(Nodo("ε"))
            return True
        nodo.agregar(Nodo("ε"))
        return True

    def parse_T(self, nodo_padre):
        nodo = nodo_padre.agregar(Nodo("T"))
        pos_respaldo = self.pos
        if self.parse_F(nodo) and self.parse_Tp(nodo):
            return True
        self.pos = pos_respaldo
        nodo_padre.hijos.remove(nodo)
        return False

    def parse_Tp(self, nodo_padre):
        nodo = nodo_padre.agregar(Nodo("T'"))
        pos_respaldo = self.pos
        tok = self.consumir("opmul")
        if tok:
            nodo.agregar(Nodo(f"opmul({tok[1]})"))
            if self.parse_F(nodo) and self.parse_Tp(nodo):
                return True
            self.pos = pos_respaldo
            nodo_padre.hijos.remove(nodo)
            nodo_padre.agregar(Nodo("T'")).agregar(Nodo("ε"))
            return True
        nodo.agregar(Nodo("ε"))
        return True

    def parse_F(self, nodo_padre):
        nodo = nodo_padre.agregar(Nodo("F"))
        pos_respaldo = self.pos

        tok = self.consumir("id")
        if tok:
            nodo.agregar(Nodo(f"id({tok[1]})"))
            return True

        tok = self.consumir("num")
        if tok:
            nodo.agregar(Nodo(f"num({tok[1]})"))
            return True

        if self.consumir("pari"):
            nodo.agregar(Nodo("pari"))
            if self.parse_E(nodo):
                if self.consumir("pard"):
                    nodo.agregar(Nodo("pard"))
                    return True

        self.pos = pos_respaldo
        nodo_padre.hijos.remove(nodo)
        return False

    def parsear(self):
        raiz = Nodo("E")
        exito = self.parse_E(raiz) and self.actual()[0] is None
        return exito, raiz


def calcular_posiciones(nodo, profundidad=0, contador=[0]):
    if not nodo.hijos:
        x = contador[0]
        contador[0] += 1
        nodo._x = x
        nodo._y = -profundidad
        return
    for hijo in nodo.hijos:
        calcular_posiciones(hijo, profundidad + 1, contador)
    nodo._x = sum(h._x for h in nodo.hijos) / len(nodo.hijos)
    nodo._y = -profundidad


def dibujar_arbol(nodo, ax):
    es_eps = nodo.etiqueta == "ε"
    es_hoja = not nodo.hijos
    color = "#E499DD" if es_eps else ("#7EC5C8" if es_hoja else "#AC4AD9")

    for hijo in nodo.hijos:
        ax.plot([nodo._x, hijo._x], [nodo._y, hijo._y],
                color="#888888", linewidth=1, zorder=1)
        dibujar_arbol(hijo, ax)

    circulo = plt.Circle((nodo._x, nodo._y), 0.35,
                          color=color, zorder=2, ec="white", linewidth=1.5)
    ax.add_patch(circulo)
    fontsize = 7 if len(nodo.etiqueta) > 6 else 8
    ax.text(nodo._x, nodo._y, nodo.etiqueta,
            ha="center", va="center", fontsize=fontsize,
            color="white", fontweight="bold", zorder=3)


def mostrar_arbol(raiz, expresion, aceptada):
    calcular_posiciones(raiz, contador=[0])

    todas = []
    def recoger(n):
        todas.append(n)
        for h in n.hijos:
            recoger(h)
    recoger(raiz)

    xs = [n._x for n in todas]
    ys = [n._y for n in todas]

    fig, ax = plt.subplots(figsize=(max(10, (max(xs) - min(xs) + 2) * 0.6),
                                    max(6,  (max(ys) - min(ys) + 2) * 1.1)))
    ax.set_aspect("equal")
    ax.axis("off")
    dibujar_arbol(raiz, ax)

    estado = "ACEPTADA" if aceptada else "RECHAZADA"
    color_titulo = "#2ecc50" if aceptada else "#e74c3c"
    ax.set_title(f'"{expresion}"  ->  {estado}',
                 fontsize=12, fontweight="bold", color=color_titulo, pad=14)

    leyenda = [
        mpatches.Patch(color="#AC4AD9", label="No terminal"),
        mpatches.Patch(color="#7EC5C8", label="Terminal"),
        mpatches.Patch(color="#E499DD", label="epsilon (vacio)"),
    ]
    ax.legend(handles=leyenda, loc="upper right", fontsize=8, framealpha=0.8)
    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(min(ys) - 1, 1.5)
    plt.tight_layout()
    nombre = re.sub(r'[^a-zA-Z0-9]', '_', expresion)[:40]
    plt.savefig(f"arbol_{nombre+str(time.time())[-2:]}.png", dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 parser.py <archivo>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lineas = f.read().splitlines()

    for linea in lineas:
        if not linea.strip():
            continue
        tokens = tokenizar(linea)
        parser = Parser(tokens)
        aceptada, arbol = parser.parsear()
        print(f'{"ACEPTADA" if aceptada else "RECHAZADA"}  "{linea}"')
        mostrar_arbol(arbol, linea, aceptada)