Actividad árbol sintáctico

Implementar un analizador sintáctico en Python para la gramática de ejemplo de las diapositivas, generando el árbol sintáctico.
   
   <img width="260" height="211" alt="image" src="https://github.com/user-attachments/assets/d5193a3d-4674-45a5-9f7e-978109a23776" />

Extrayendo del capítulo 4 del libro Compiladores para realizar la implementación de ASD con retroceso (recursivo).

Como se explica en el libro, las gramáticas deben cumplir tres condiciones para poder aplicarse análisis descendente, que no sean ambiguas, que no tengan recursión por izquierda y que no les falte factorización por izquierda. De entre estas condiciones, la gramática proporcionada falla en recursión por izquierda, por lo que se modifica en ese sentido para poder proceder.

   E → T E'
   
   E' → opsuma T E' | ε
   
   T → F T'
   
   T' → opmul F T' | ε
   
   F → id
   
   F → num
   
   F → pari E pard

Ya con la gramática corregida se procede creando las funciones para realizar el parseo.
