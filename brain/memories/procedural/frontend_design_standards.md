# Procedimento Operacional Padrao (SOP): frontend_design_standards
Objetivo: Padrao estetico oficial para interfaces web de Guilherme Gustavo Weber — **Tactile Soft-Neumorphic & Editorial Teal (Potadot Standard)**. Combina superficie clara aveludada (`--paper`), sombras direcionais esculpidas (elevacao e cavidade), blocos de contraste em verde-petroleo profundo (`--teal`), tipografia geometrica fluida e micro-interacoes cineticas.

---

## 1. Tokens Fundamentais (`:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap');

:root {
  /* Paleta Editorial & Contraste — Dark Potadot (Padrao) */
  --paper: #071417;        /* Superficie base escura (Teal-Obsidian profundo) */
  --paper-2: #0B1E22;      /* Superficie secundaria */
  --card: #0E252B;         /* Superficie elevada */
  --white: #122E35;        /* Tiles internos e destaques */
  --ink: #EAF4EE;          /* Texto primario (sage off-white) */
  --ink-2: #B8D0C8;        /* Texto secundario */
  --muted: #7FA198;        /* Metadados e legendas */
  --green: #3DB663;        /* Acento primario (Emerald vivo) */
  --green-ink: #52D67C;    /* Verde luminoso para leitura sobre fundo escuro */
  --green-soft: rgba(61, 182, 99, 0.16);
  --teal: #030A0C;         /* Blocos de contraste abissal (.on-dark / mockups / footer) */
  --teal-2: #091B1F;
  --brown: #E09F67;        /* Acento cobre/ambar para subtitulos de preco */
  --peach: #E5BA97;        /* Acento quente para indicadores e dots */
  --line: rgba(234, 244, 238, .09);
  --on-dark: #EAF4EE;
  --on-dark-muted: #9FB9B1;

  /* Sistema Triplo de Sombras Tateis Escuras (Elevacao & Cavidade) */
  --shadow-raise: 12px 12px 28px rgba(1, 5, 6, .78), -8px -8px 22px rgba(22, 62, 70, .25), inset 0 1px 0 rgba(234, 244, 238, .08);
  --shadow-soft:  6px 6px 16px rgba(1, 5, 6, .65), -5px -5px 14px rgba(22, 62, 70, .2), inset 0 1px 0 rgba(234, 244, 238, .06);
  --shadow-press: inset 6px 6px 14px rgba(1, 5, 6, .82), inset -5px -5px 12px rgba(22, 62, 70, .22);

  /* Tipografia & Curva de Animacao */
  --f-display: "Outfit", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --f-body: "Figtree", "Segoe UI", system-ui, -apple-system, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, monospace;
  --ease: cubic-bezier(.22, 1, .36, 1);
}

/* Variante Clara Opcional via html[data-theme="light"] */
html[data-theme="light"] {
  --paper: #F2F3F7; --paper-2: #E9EBF1; --card: #F7F8FB; --white: #FFFFFF;
  --ink: #1F1C1D; --ink-2: #3A3F47; --muted: #646B76;
  --green-ink: #23874A; --green-soft: #DDF2E4; --teal: #0A282D; --brown: #B07040;
  --shadow-raise: 12px 12px 28px rgba(160, 166, 186, .42), -12px -12px 28px rgba(255, 255, 255, .95);
  --shadow-soft:  6px 6px 16px rgba(160, 166, 186, .35), -6px -6px 16px rgba(255, 255, 255, .9);
  --shadow-press: inset 6px 6px 14px rgba(160, 166, 186, .38), inset -6px -6px 14px rgba(255, 255, 255, .95);
}
```

---

## 2. Regras Arquiteturais e Componentes de Assinatura

1. **Fisicalidade Tatil (Elevacao vs. Cavidade)**:
   - **Cards e Painel Principal**: `background: var(--paper); box-shadow: var(--shadow-raise); border-radius: 28px–36px; border: 0`.
   - **Inputs, Campos de Busca, Trilhos de Filtro e Palco de Icones**: usam `box-shadow: var(--shadow-press)` para parecerem esculpidos dentro da superficie `--paper`. No `:focus`, adicionam `0 0 0 2px var(--green)`.
2. **Navbar Flutuante em Pilula**:
   - Destacada do topo (`top: 14px`, `border-radius: 999px`), `background: rgba(242, 243, 247, 0.82)`, `backdrop-filter: blur(16px) saturate(1.4)`, `box-shadow: 0 1px rgba(255,255,255,.85) inset, 0 12px 32px rgba(10,40,45,.09)`.
   - Link ativo marcado com ponto inferior `5x5px` em `var(--green)`.
3. **Eyebrow com Ponto Duplo & Dot-End**:
   - `.eyebrow` em `var(--f-mono)` uppercase (`letter-spacing: .12em`, `color: var(--green-ink)`), precedido por `:before` circular (`8x8px`, `background: var(--green)`, `box-shadow: 14px 0 0 -1px var(--peach)`).
   - Titulos principais (`h1.dot-end`) encerrados com ponto verde inline (`width: .2em; height: .2em; background: var(--green)`).
4. **Botoes Cineticos (`.btn`)**:
   - Formato pilula (`border-radius: 999px`, `background: var(--ink)`, `color: var(--white)`).
   - **Cortina no Hover (`.btn::before`)**: camada `background: var(--green)` que sobe de `translateY(101%)` para `translateY(0)` em `.5s var(--ease)`.
   - **Texto Rolante (`.btn-t > span[data-t]`)**: sobe `translateY(-105%)` revelando o texto secundario no `::after`.
   - **Icone Circular (`.btn-ico`)**: `30x30px` em `var(--green)` que gira `transform: rotate(-45deg)` e muda para `var(--ink)` no hover.
5. **Blocos de Contraste Deep-Teal (`.on-dark` / `.hero-hud-card`)**:
   - Janelas de telemetria, mockups, rodape e toasts usam `background: var(--teal)` (`#0A282D`) com malha radial de pontos verdes (`radial-gradient(rgba(61,182,99,.35) 1.2px, transparent 1.6px)` com `background-size: 22px 22px`), dots de janela (`--peach`, `--brown`, `--green`) e cards flutuantes brancos com `animation: mkFloat 4.2s ease-in-out infinite`.
6. **Textura Film-Grain Global (`body::after`) & Spotlight de Cursor**:
   - Overlay fixo com SVG `<feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/>` em `opacity: .042` para aspecto organico de papel impresso.
   - Cards rastreiam `--mx` e `--my` via `pointermove` aplicando `radial-gradient(420px circle at var(--mx) var(--my), rgba(61, 182, 99, .12), transparent 45%)`.
7. **Fundo Arquitetonico em 4 Camadas (`body`, `body::before` e `.bg-stage`)**:
   - **Malha CAD + Dot Matrix (`body::before`)**: Matriz de micro-pontos esmeralda (`28x28px`) combinada a linhas de blueprint (`140x140px`) com `mask-image` eliptica.
   - **Auroras Ambientes + Feixe de Cursor (`body`)**: Focos difusos (`--green`, `--peach` e petroleo profundo) somados a um feixe radial de `650px` guiado por `--page-mx` e `--page-my`.
   - **Orbes, Aneis e Miras Flutuantes (`.bg-stage`)**: Esferas neumorficas (`.bg-orb`), aneis vazados (`.bg-orb--ring`) com animacao `bgOrbFloat` e miras de telemetria (`.bg-crosshair`).
8. **Palco Fotografico de Produto (`.card-visual`)**:
   - Container esculpido (`height: 215px`, `border-radius: 22px`, `box-shadow: var(--shadow-press)`) com foto full-bleed (`.card-img`, `scale(1.07)` no hover), vinheta editorial escura (`.card-visual::after`) e selo tatil SVG flutuante no canto inferior direito (`right: 12px; bottom: 12px`).
