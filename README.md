# Árbol Sintáctico — Analizador Descendente con Retroceso

Implementación de un analizador sintáctico descendente con retroceso en Python, basado en el capítulo 4 del libro *Compiladores*. El analizador procesa expresiones aritméticas, determina si pertenecen al lenguaje de la gramática y genera el árbol sintáctico correspondiente de forma visual.

---

## Gramática

La gramática original presenta recursión por izquierda, condición que impide aplicar análisis descendente. Siguiendo los criterios del libro, se verifica que la gramática cumpla tres condiciones: que no sea ambigua, que no tenga recursión por izquierda y que tenga factorización por izquierda. Al fallar en recursión por izquierda, se transforma obteniendo la siguiente gramática equivalente libre de esa condición:

```
E  → T E'
E' → opsuma T E' | ε
T  → F T'
T' → opmul F T' | ε
F  → id | num | pari E pard
```

---

## Implementación

El analizador se implementa como un parser recursivo descendente con retroceso. Cada no terminal de la gramática corresponde a una función (`parse_E`, `parse_Ep`, `parse_T`, `parse_Tp`, `parse_F`) que intenta consumir tokens y construir el árbol. Si una producción falla, el parser retrocede y prueba la siguiente alternativa.

El árbol sintáctico se visualiza con `matplotlib`, usando colores diferenciados para nodos no terminales, terminales y producciones vacías (ε).

---

## Requisitos

```
matplotlib
```

Instalar con:

```bash
pip install -r requisitos.txt
```

---

## Uso

```bash
python3 arbol_sintactico.py entrada.txt
```

Por cada línea del archivo se imprime el resultado en consola y se guarda una imagen `.png` del árbol sintáctico en el directorio actual.

---

## Entradas de prueba

### `2+3*4` — ACEPTADA

<img width="1326" height="1302" alt="arbol_2_3_457" src="https://github.com/user-attachments/assets/c9c82f34-7951-4198-8094-1af0258bf71b" />


### `2+3*(4-5)` — ACEPTADA

<img width="1485" height="1214" alt="arbol_2_3__4_5_64" src="https://github.com/user-attachments/assets/8a24e4f5-3751-487d-a0a7-e8486b4327dd" />



### `2+3-4` — ACEPTADA

<img width="1485" height="1314" alt="arbol_2_3_473" src="https://github.com/user-attachments/assets/d28ecb41-db66-4ad3-bdf8-e5fa09b215df" />


### `a++b` — RECHAZADA

<img width="580" height="973" alt="arbol_a__b18" src="https://github.com/user-attachments/assets/8d3120e0-ab97-45ec-951b-bf8f9d6bdc1e" />


### `(a+b)*(c+d)/2-6` — ACEPTADA

<img width="2235" height="1092" alt="arbol__a_b___c_d__2_619" src="https://github.com/user-attachments/assets/caa1123a-3a28-409a-a449-1c24b52aed30" />


---

## Estructura del proyecto

```
├── arbol_sintactico.py   # Analizador sintáctico y visualizador
├── entrada.txt           # Casos de prueba
├── requisitos.txt        # Dependencias
└── README.md
```
