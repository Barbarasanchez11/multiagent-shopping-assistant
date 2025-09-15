# 🎤 Guión de Presentación - Asistente Multi-Agente de Compras

## 📋 Estructura de la Presentación (15-20 minutos)

---

## 🎯 **1. INTRODUCCIÓN (2 minutos)**

### **Hook inicial:**
> "¿Cuántas veces han ido al supermercado con una lista mental como 'necesito agua, arroz y pan' y han terminado gastando más de lo planeado o comprando productos que no necesitaban?"

### **Presentación del problema:**
- **Problema real:** Convertir listas de compras mentales en productos específicos con precios
- **Dificultad:** Cada supermercado tiene diferentes productos, marcas y precios
- **Solución:** IA conversacional + web scraping inteligente

### **Demo rápido:**
> "Les voy a mostrar cómo funciona en tiempo real..."

---

## 🚀 **2. DEMO EN VIVO (5 minutos)**

### **Preparación:**
```bash
# Terminal 1
python mock_api.py

# Terminal 2  
streamlit run app.py
```

### **Demo paso a paso:**
1. **Abrir la aplicación:** http://localhost:8501
2. **Escribir lista:** "2 de agua, 3 kg de arroz integral, un pan de centeno"
3. **Mostrar búsqueda:** Explicar que está buscando en tiempo real
4. **Mostrar opciones:** Explicar las diferentes opciones de productos
5. **Ajustar cantidades:** Mostrar la flexibilidad
6. **Ver total:** Mostrar cálculo en tiempo real
7. **Descargar ticket:** Mostrar exportación TXT/JSON

### **Puntos clave a destacar:**
- ✅ **Entrada natural:** Escribes como hablas
- ✅ **Búsqueda inteligente:** Encuentra productos aunque no coincida exactamente
- ✅ **Múltiples opciones:** Te da opciones para elegir
- ✅ **Cálculo automático:** Ve el total mientras seleccionas

---

## 🏗️ **3. ARQUITECTURA TÉCNICA (5 minutos)**

### **Mostrar diagrama de flujo:**
```
Usuario → Streamlit → LangGraph → 3 Agentes → API Mock → Resultado
```

### **Explicar los 3 agentes:**

#### **🤖 Agente 1: Clasificador de Intención**
- **¿Qué hace?** Convierte texto natural a datos estructurados
- **Tecnología:** Groq LLM (llama-3.1-8b-instant)
- **Ejemplo:** "2 de agua" → `{"name": "agua", "quantity": 2}`

#### **🛍️ Agente 2: Buscador Mercadona**
- **¿Qué hace?** Encuentra productos reales con precios
- **Tecnología:** Playwright + técnicas anti-detección
- **Características:**
  - Rotación de navegadores
  - Delays inteligentes
  - Simulación de comportamiento humano
  - Fallback a datos mock si falla

#### **💰 Agente 3: Calculadora de Precios**
- **¿Qué hace?** Selecciona la mejor opción y calcula totales
- **Lógica:** Automáticamente elige la opción más barata

### **Mostrar código clave:**
```python
# Ejemplo del flujo de agentes
graph.add_node("intent_classifier", classify_intent_agent)
graph.add_node("mercadona_search", mercadona_search_agent)  
graph.add_node("total_price", total_price_agent)
```

---

## 💡 **4. INNOVACIONES TÉCNICAS (3 minutos)**

### **🛡️ Anti-Detección Avanzada:**
- **Problema:** Los sitios web bloquean bots
- **Solución:** Simulación de navegación humana real
- **Técnicas:**
  - 8 User-Agents diferentes
  - Delays aleatorios (2.5-8 segundos)
  - Movimientos de mouse y scroll
  - Headers realistas con huellas digitales

### **🧠 Matching Inteligente:**
- **Problema:** "azúcar" debe encontrar "azúcar blanco Hacendado"
- **Solución:** Algoritmos de similitud semántica
- **Resultado:** Encuentra productos aunque el nombre no coincida exactamente

### **🔄 Sistema Robusto:**
- **Fallback automático:** Si falla la API real, usa datos mock
- **Manejo de errores:** Reintentos inteligentes
- **Estado persistente:** Mantiene contexto entre agentes

---

## 🎨 **5. INTERFAZ DE USUARIO (2 minutos)**

### **Diseño moderno:**
- **Tema oscuro** profesional
- **Cards de productos** con información clara
- **Sidebar de resumen** siempre visible
- **Cálculo en tiempo real**

### **Experiencia de usuario:**
- **Input natural:** Escribe como hablarías
- **Selección visual:** Dropdowns intuitivos
- **Feedback inmediato:** Ve el total mientras seleccionas
- **Exportación fácil:** Un click para descargar

---

## 📊 **6. CASOS DE USO REALES (2 minutos)**

### **Caso 1: Lista Básica**
```
Input: "pan, leche, huevos"
Output: 3 productos, total: 4.50€
```

### **Caso 2: Lista Compleja**
```
Input: "2 de agua, 3 kg de arroz integral, leche sin lactosa"
Output: Múltiples opciones por producto
```

### **Caso 3: Productos Específicos**
```
Input: "aceite de oliva virgen extra"
Output: Productos premium con precios diferenciados
```

---

## 🚀 **7. TECNOLOGÍAS Y STACK (1 minuto)**

### **Backend:**
- **LangGraph:** Orquestación de agentes
- **Groq LLM:** Procesamiento de lenguaje natural
- **Playwright:** Web scraping avanzado
- **FastAPI:** API mock
- **Pydantic:** Validación de datos

### **Frontend:**
- **Streamlit:** Interfaz web interactiva
- **CSS personalizado:** Diseño moderno

### **Infraestructura:**
- **Poetry:** Gestión de dependencias
- **Async/await:** Procesamiento asíncrono

---

## 🔮 **8. FUTURO Y EXTENSIONES (1 minuto)**

### **Posibles mejoras:**
1. **Más supermercados:** Carrefour, Lidl, etc.
2. **Comparación de precios:** Entre diferentes tiendas
3. **Recomendaciones:** Productos similares
4. **Historial:** Listas anteriores
5. **Integración:** Apps de delivery

---

## 🎯 **9. CONCLUSIÓN (1 minuto)**

### **Valor del proyecto:**
- **Técnico:** Arquitectura multi-agente escalable
- **Práctico:** Herramienta útil para el día a día
- **Educativo:** Integración de múltiples tecnologías

### **Mensaje final:**
> "Este proyecto demuestra cómo la IA conversacional puede combinarse con web scraping inteligente para crear soluciones prácticas que resuelven problemas reales."

---

## ❓ **10. PREGUNTAS Y RESPUESTAS (5 minutos)**

### **Preguntas frecuentes esperadas:**

**Q: ¿Por qué usar múltiples agentes en lugar de uno solo?**
A: Cada agente tiene una responsabilidad específica. Esto hace el sistema más mantenible, escalable y fácil de debuggear.

**Q: ¿Qué pasa si Mercadona cambia su sitio web?**
A: El sistema tiene fallback automático a datos mock, y la arquitectura modular permite actualizar solo el agente de búsqueda.

**Q: ¿Se puede integrar con otros supermercados?**
A: Sí, solo necesitaríamos crear nuevos agentes de búsqueda para cada supermercado.

**Q: ¿Cómo maneja productos que no encuentra?**
A: El sistema de matching inteligente encuentra productos similares, y si no encuentra nada, lo indica claramente al usuario.

**Q: ¿Es escalable para muchos usuarios?**
A: Sí, cada agente es independiente y se puede escalar horizontalmente.

---

## 🛠️ **MATERIALES DE APOYO**

### **Archivos a tener listos:**
- ✅ `PRESENTACION_PROYECTO.md` - Documentación completa
- ✅ `DIAGRAMA_FLUJO.txt` - Diagrama visual
- ✅ `app.py` - Código de la interfaz
- ✅ `mock_api.py` - API mock funcionando
- ✅ Screenshots de la aplicación

### **Comandos de demo:**
```bash
# Terminal 1: API Mock
python mock_api.py

# Terminal 2: Aplicación
streamlit run app.py
```

### **URLs importantes:**
- **Aplicación:** http://localhost:8501
- **API Mock:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs

---

## 💡 **TIPS PARA LA PRESENTACIÓN**

1. **Empieza con el demo:** Captura la atención inmediatamente
2. **Explica la tecnología después:** Una vez que ven el valor, explican cómo funciona
3. **Usa ejemplos reales:** "Imaginen que van a hacer la compra..."
4. **Muestra el código:** Pero no te pierdas en detalles
5. **Termina con el futuro:** Deja a la audiencia pensando en las posibilidades

¡Éxito en tu presentación! 🚀
