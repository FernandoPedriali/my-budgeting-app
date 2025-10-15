# 🎨 Design System - My Budgeting App

Guia de estilos e componentes visuais do projeto.

---

## 📐 Fundamentos

### Paleta de Cores

#### **Cores Principais**
- **Primary (Azul)**: `#3B82F6` - Ações principais, links, destaque
- **Secondary (Roxo)**: `#8B5CF6` - Elementos secundários, variações

#### **Cores Funcionais**
- **Success (Verde)**: `#10B981` - Confirmações, receitas
- **Warning (Amarelo)**: `#F59E0B` - Avisos, alertas
- **Error (Vermelho)**: `#EF4444` - Erros, despesas, exclusões
- **Info (Ciano)**: `#06B6D4` - Informações

#### **Cores de Contexto**
- **Income (Receitas)**: `#10B981` com background `#D1FAE5`
- **Expense (Despesas)**: `#EF4444` com background `#FEE2E2`

#### **Cores Neutras (Light Mode)**
- Background Primary: `#FFFFFF`
- Background Secondary: `#F9FAFB`
- Background Tertiary: `#F3F4F6`
- Text Primary: `#111827`
- Text Secondary: `#6B7280`
- Text Tertiary: `#9CA3AF`
- Border: `#E5E7EB`

#### **Dark Mode**
- Background Primary: `#111827`
- Background Secondary: `#1F2937`
- Background Tertiary: `#374151`
- Text Primary: `#F9FAFB`
- Text Secondary: `#D1D5DB`
- Text Tertiary: `#9CA3AF`
- Border: `#374151`

---

## 📝 Tipografia

### **Font Family**
- **Sans-serif**: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- **Monospace**: ui-monospace, SFMono-Regular, 'SF Mono', Consolas, monospace

### **Tamanhos de Fonte**
- **xs**: 12px (0.75rem) - Captions, labels pequenos
- **sm**: 14px (0.875rem) - Body secundário, botões
- **base**: 16px (1rem) - Body principal
- **lg**: 18px (1.125rem) - Body grande
- **xl**: 20px (1.25rem) - Subtítulos
- **2xl**: 24px (1.5rem) - Headings pequenos
- **3xl**: 30px (1.875rem) - Headings médios
- **4xl**: 36px (2.25rem) - Headings grandes
- **5xl**: 48px (3rem) - Títulos principais

### **Pesos de Fonte**
- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700
- **Extrabold**: 800

### **Uso Recomendado**
```
H1: 36px, Bold, Line Height 1.25
H2: 30px, Bold, Line Height 1.25
H3: 24px, Semibold, Line Height 1.375
H4: 20px, Semibold, Line Height 1.375
H5: 18px, Medium, Line Height 1.5
H6: 16px, Medium, Line Height 1.5

Body Large: 18px, Regular, Line Height 1.625
Body: 16px, Regular, Line Height 1.5
Body Small: 14px, Regular, Line Height 1.5
Caption: 12px, Regular, Line Height 1.5

Button Large: 16px, Semibold
Button: 14px, Semibold
Button Small: 12px, Semibold
```

---

## 📏 Espaçamento

### **Sistema Base (múltiplos de 4px)**
- **xs**: 4px (0.25rem)
- **sm**: 8px (0.5rem)
- **md**: 16px (1rem)
- **lg**: 24px (1.5rem)
- **xl**: 32px (2rem)
- **2xl**: 40px (2.5rem)
- **3xl**: 48px (3rem)
- **4xl**: 64px (4rem)
- **5xl**: 96px (6rem)
- **6xl**: 128px (8rem)

### **Uso nos Componentes**
- **Card Padding**: 24px (lg)
- **Modal Padding**: 32px (xl)
- **Form Field Gap**: 16px (md)
- **Button Padding**: 8px vertical, 24px horizontal
- **Input Padding**: 8px vertical, 16px horizontal
- **Section Gap**: 40px (2xl)
- **Page Padding**: 32px (xl)

---

## 🔲 Border Radius

- **sm**: 4px - Pequenos elementos
- **md**: 6px - Inputs, badges
- **lg**: 8px - Cards, botões
- **xl**: 12px - Modais
- **2xl**: 16px - Elementos grandes
- **3xl**: 24px - Elementos especiais
- **full**: 9999px - Círculos, pills

---

## 🎯 Componentes

### **Card**
```
Background: bg-primary
Border: 1px solid border-color
Border Radius: lg (8px)
Padding: lg (24px)
Shadow: sm
Hover: shadow-md
```

### **Button - Primary**
```
Background: primary (#3B82F6)
Color: white
Padding: 8px 24px
Font: 14px, Semibold
Border Radius: md (6px)
Height: 40px (md)
Shadow: none → md on hover
```

### **Button - Variants**
- **Success**: Background green-500
- **Error**: Background red-500
- **Warning**: Background amber-500
- **Secondary**: Background gray-200, text-primary

### **Input**
```
Background: bg-primary
Border: 1px solid border-color
Border Radius: md (6px)
Padding: 8px 16px
Height: 40px (md)
Focus: border-primary + shadow (0 0 0 3px primary/10%)
```

### **Badge**
```
Padding: 2px 8px
Font: 12px, Medium
Border Radius: full
Height: auto

- Success: bg-green-100, text-green-700
- Error: bg-red-100, text-red-700
- Warning: bg-amber-100, text-amber-700
- Info: bg-blue-100, text-blue-700
```

### **Modal**
```
Background: bg-primary
Border Radius: xl (12px)
Padding: xl (32px)
Shadow: lg
Max Width: 640px (sm container)
Backdrop: rgba(0,0,0,0.5)
```

### **Data Table**
```
Background: bg-primary
Border: 1px solid border-color
Border Radius: lg (8px)

Header:
  - Background: bg-secondary
  - Font: 14px, Semibold
  - Padding: 12px 16px

Row:
  - Padding: 12px 16px
  - Border Bottom: 1px solid border-color
  - Hover: bg-secondary
```

---

## 🎭 Estados Visuais

### **Hover**
- Botões: Escurecer cor + adicionar shadow-md
- Cards: Adicionar shadow-md
- Links: Sublinhar
- Inputs: border-primary

### **Focus**
- Inputs: border-primary + shadow (ring)
- Botões: outline de 2px primary com offset

### **Disabled**
- Opacidade: 50%
- Cursor: not-allowed
- Sem hover effects

### **Loading**
- Spinner: primary color
- Skeleton: bg-tertiary com animação pulse

---

## 📱 Responsividade

### **Breakpoints**
- **sm**: 640px - Tablets pequenos
- **md**: 768px - Tablets
- **lg**: 1024px - Laptops
- **xl**: 1280px - Desktops
- **2xl**: 1536px - Telas grandes

### **Grid System**
- 12 colunas
- Gap padrão: 16px (md)

### **Sidebar**
- Desktop: 256px (16rem)
- Colapsada: 64px (4rem)
- Mobile: Drawer overlay

---

## 🎨 Ícones

### **Biblioteca**: Material Icons (via NiceGUI/Quasar)

### **Tamanhos**
- **xs**: 16px
- **sm**: 20px
- **md**: 24px (padrão)
- **lg**: 32px
- **xl**: 40px

### **Ícones Principais**
- **Home**: `home`
- **Categorias**: `label`, `folder`
- **Contas**: `wallet`, `credit_card`, `bank`
- **Transações**: `arrow_upward` (receita), `arrow_downward` (despesa)
- **Adicionar**: `add`
- **Editar**: `edit`
- **Deletar**: `delete`
- **Filtrar**: `filter_list`
- **Buscar**: `search`
- **Configurações**: `settings`

---

## ✨ Animações

### **Transições**
- Padrão: `transition: all 0.2s ease`
- Hover: 200ms
- Focus: 200ms

### **Keyframes**
```css
fadeIn: opacity 0 → 1 (300ms)
slideInUp: translateY(20px) → 0 + opacity (300ms)
pulse: scale 1 → 1.05 → 1 (loop)
```

---

## 🎯 Uso no Código

### **Python (Theme)**
```python
from frontend.app.theme import light_colors, spacing, typography

# Cores
color = light_colors.primary

# Espaçamento
padding = spacing.lg

# Tipografia
font_size = typography.size.xl
```

### **CSS (Variáveis)**
```css
.my-element {
  color: var(--color-primary);
  padding: var(--spacing-lg);
  font-size: var(--font-size-xl);
  border-radius: var(--radius-lg);
}
```

---

## 📦 Checklist de Componentes

### **Fase H - Componentes Base** (Próxima fase)
- [ ] Card
- [ ] Button (variants)
- [ ] Input (text, number, date, select)
- [ ] Modal
- [ ] DataTable
- [ ] Loader
- [ ] Alert
- [ ] Badge
- [ ] EmptyState
- [ ] CurrencyInput
- [ ] ColorPicker
- [ ] IconPicker
- [ ] ConfirmDialog

---

## 🎨 Exemplos Visuais

### **Cartão de Conta**
```
┌─────────────────────────────────────┐
│  💳 Nubank                     ⋮    │
│                                     │
│  Saldo Atual                        │
│  R$ 4.500,00                        │
│                                     │
│  [💚 Receita] [🔴 Despesa]          │
└─────────────────────────────────────┘
```

### **Lista de Transações**
```
┌──────────────────────────────────────────────┐
│ Data       │ Descrição    │ Categoria │ Valor │
├──────────────────────────────────────────────┤
│ 13/10/2025 │ Salário      │ 💰 Renda  │ +5000 │
│ 12/10/2025 │ Supermercado │ 🛒 Comida │ -250  │
│ 11/10/2025 │ Uber         │ 🚗 Trans. │ -30   │
└──────────────────────────────────────────────┘
```

---

**Última atualização**: Fase B - Sprint 1
