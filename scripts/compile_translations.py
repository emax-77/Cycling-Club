from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    try:
        import polib
    except Exception:
        print('Missing dependency: polib')
        print('Install: py -m pip install polib')
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    locale_root = repo_root / 'locale'

    if not locale_root.exists():
        print(f'No locale directory: {locale_root}')
        return 0

    po_files = sorted(locale_root.glob('*/LC_MESSAGES/*.po'))
    if not po_files:
        print(f'No .po files found under: {locale_root}')
        return 0

    changed = 0
    for po_path in po_files:
        mo_path = po_path.with_suffix('.mo')
        catalog = polib.pofile(str(po_path))
        catalog.save_as_mofile(str(mo_path))
        changed += 1
        print(f'Wrote {mo_path.relative_to(repo_root)}')

    print(f'Done ({changed} file(s)).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
