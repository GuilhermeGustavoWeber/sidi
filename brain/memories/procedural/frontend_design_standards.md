# Procedimento Operacional Padrao (SOP): frontend_design_standards
Objetivo: Padrao estetico oficial para interfaces web de Guilherme Gustavo Weber — **Tactile Soft-Neumorphic & Editorial Teal (Potadot Standard)**. Combina superficie clara aveludada (`--paper`), sombras direcionais esculpidas (elevacao e cavidade), blocos de contraste em verde-petroleo profundo (`--teal`), tipografia geometrica fluida e micro-interacoes cineticas.

---

## 1. Tokens Fundamentais (`:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap');

:root {
  /* Paleta Editorial & Contraste */
  --paper: #F2F3F7;        /* Superficie base (papel frio aveludado) */
  --paper-2: #E9EBF1;      /* Superficie secundaria */
  --card: #F7F8FB;         /* Superficie elevada */
  --ink: #1F1C1D;          /* Texto primario (quase preto quente) */
  --ink-2: #3A3F47;        /* Texto secundario */
  --muted: #646B76;        /* Metadados e legendas */
  --green: #3DB663;        /* Acento primario (Emerald vivo) */
  --green-ink: #23874A;    /* Verde escuro para leitura sobre fundo claro */
  --green-soft: #DDF2E4;   /* Fundo de badges/pills */
  --teal: #0A282D;         /* Blocos de alto contraste (.on-dark / mockups / footer / toasts) */
  --teal-2: #123A3B;       /* Elevacao sobre --teal */
  --brown: #B07040;        /* Acento terroso para subtitulos de preco/destaques */
  --peach: #E5BA97;        /* Acento quente para indicadores e dots */
  --white: #FFFFFF;
  --line: rgba(10, 40, 45, .09);
  --on-dark: #EAF4EE;
  --on-dark-muted: #9FB9B1;

  /* Sistema Triplo de Sombras Tateis (Sem bordas duras) */
  --shadow-raise: 12px 12px 28px rgba(160, 166, 186, .42), -12px -12px 28px rgba(255, 255, 255, .95);
  --shadow-soft:  6px 6px 16px rgba(160, 166, 186, .35), -6px -6px 16px rgba(255, 255, 255, .9);
  --shadow-press: inset 6px 6px 14px rgba(160, 166, 186, .38), inset -6px -6px 14px rgba(255, 255, 255, .95);

  /* Tipografia & Curva de Animacao */
  --f-display: "Outfit", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --f-body: "Figtree", "Segoe UI", system-ui, -apple-system, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, monospace;
  --ease: cubic-bezier(.22, 1, .36, 1);
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
