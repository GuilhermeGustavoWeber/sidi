# Procedimento Operacional Padrao (SOP): frontend_design_standards
Objetivo: Garantir padrao estetico moderno, layout eficiente, dinamico e de alto valor visual para interfaces web (HTML/CSS/JS).

## Diretrizes de Design Obrigatorias
1. **Paleta Visual**: Dark theme obsidian/slate (`#090d16`, `#0f172a`), com acentos luminosos ciano/indigo (`#38bdf8`, `#818cf8`) e degradês sutis em titulos.
2. **Vidro Fosco e Profundidade (Glassmorphism)**: `backdrop-filter: blur(16px)` para barras de navegacao, drawers e modais, combinados com bordas ultrafinas (`1px solid rgba(255, 255, 255, 0.08)`).
3. **Layout Dinamico**:
   - Off-canvas drawers para carrinhos e paineis laterais em vez de caixas pop-up estaticas.
   - Micro-interacoes com hover lifts (`translateY(-2px)` a `-4px`), transicoes cubic-bezier (`all 0.25s cubic-bezier(0.16, 1, 0.3, 1)`).
   - Busca em tempo real e filtros rapidos via chips.
4. **Sem Dependencias Pesadas de CDN**: Interfaces leves, renderizacao instantanea, SVGs nativos para iconografia e responsividade completa para mobile e desktop.
5. **Feedback Imediato ao Usuario**: Toasts animados com auto-dismiss para confirmacao de acoes sem bloquear o fluxo.
