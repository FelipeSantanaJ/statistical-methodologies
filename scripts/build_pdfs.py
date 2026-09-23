"""Gera os PDFs combinados em pdf/{pt,en}/ a partir dos .md de cada metodologia.

Requer pandoc + um motor LaTeX (xelatex, via MiKTeX ou TeX Live) no PATH.
Rodar da raiz do repositório:

    python scripts/build_pdfs.py            # os dois idiomas
    python scripts/build_pdfs.py pt          # só um idioma
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
AUTOR = "Felipe Santana"

# ordem canônica: a mesma das categorias no README.md e da visão geral nível 1
METODOS = [
    "welch-t-test", "oaxaca-blinder", "rif-decomposition",
    "inequality-decomposition", "duncan-index",
    "structural-break", "diff-in-diff", "panel-transitions",
    "ab-testing", "srm-test", "covariate-balance", "non-inferiority",
    "heterogeneity-testing", "power-mde", "spillover-cannibalization",
    "cluster-robust-se", "randomization-inference", "wild-cluster-bootstrap",
    "cohort-retention-decomposition", "growth-decomposition",
    "poisson-regression", "wls-trend", "logistic-regression",
]

IDIOMAS = {
    "pt": {
        "nivel1": "simplificado/visao-geral.md",
        "nivel2_dir": "metodologias", "nivel3_dir": "completo",
        "titulo_nivel1": "Visão geral — todas as metodologias, em linguagem simples",
        "titulo_nivel2": "Metodologias, nível 2 — intuição e uso",
        "titulo_nivel3": "Metodologias, nível 3 — formulação completa",
        "saida": {"nivel1": "visao-geral.pdf", "nivel2": "metodologias-nivel2.pdf", "nivel3": "metodologias-nivel3.pdf"},
    },
    "en": {
        "nivel1": "simplified/overview.md",
        "nivel2_dir": "methodologies", "nivel3_dir": "complete",
        "titulo_nivel1": "Overview — every methodology, in plain language",
        "titulo_nivel2": "Methodologies, level 2 — intuition and usage",
        "titulo_nivel3": "Methodologies, level 3 — full formulation",
        "saida": {"nivel1": "overview.pdf", "nivel2": "methodologies-level2.pdf", "nivel3": "methodologies-level3.pdf"},
    },
}

_RE_IMG = re.compile(r"\]\(((?:\.\./)+assets/[^)]+)\)")


def _rebasear_imagens(texto: str, origem: Path) -> str:
    """Reescreve caminhos relativos de imagem para serem relativos à raiz do repo."""
    def troca(m: re.Match) -> str:
        alvo = (origem.parent / m.group(1)).resolve()
        return f"]({alvo.relative_to(RAIZ).as_posix()})"
    return _RE_IMG.sub(troca, texto)


_LANG_TAG = {"pt": "pt-BR", "en": "en-US"}


def _montar(arquivos: list[Path], titulo: str, idioma: str) -> str:
    partes = [f'---\ntitle: "{titulo}"\nauthor: "{AUTOR}"\nlang: "{_LANG_TAG[idioma]}"\n---\n']
    for i, arq in enumerate(arquivos):
        if i > 0:
            partes.append("\n```{=latex}\n\\clearpage\n```\n")
        partes.append(_rebasear_imagens(arq.read_text(encoding="utf-8"), arq))
    return "\n".join(partes)


def _pandoc(md_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pandoc", str(md_path.name), "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--toc", "--toc-depth=1",
        "-V", "geometry:margin=1in",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "fontsize=11pt",
    ]
    subprocess.run(cmd, cwd=RAIZ, check=True)
    print(f"  {pdf_path.relative_to(RAIZ)}")


def gerar(idioma: str) -> None:
    cfg = IDIOMAS[idioma]
    docs = RAIZ / "docs" / idioma
    pdf_dir = RAIZ / "pdf" / idioma
    tmp = RAIZ / "_tmp_build_pdf.md"

    tmp.write_text(_montar([docs / cfg["nivel1"]], cfg["titulo_nivel1"], idioma), encoding="utf-8")
    _pandoc(tmp, pdf_dir / cfg["saida"]["nivel1"])

    for chave, nivel_dir in (("nivel2", cfg["nivel2_dir"]), ("nivel3", cfg["nivel3_dir"])):
        arquivos = [docs / nivel_dir / f"{m}.md" for m in METODOS]
        faltando = [str(a) for a in arquivos if not a.exists()]
        if faltando:
            raise FileNotFoundError(f"faltando: {faltando}")
        tmp.write_text(_montar(arquivos, cfg[f"titulo_{chave}"], idioma), encoding="utf-8")
        _pandoc(tmp, pdf_dir / cfg["saida"][chave])

    tmp.unlink(missing_ok=True)


def main() -> None:
    idiomas = sys.argv[1:] or list(IDIOMAS)
    for idioma in idiomas:
        print(f"{idioma}:")
        gerar(idioma)


if __name__ == "__main__":
    main()
