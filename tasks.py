

def run(*p, **k):
    from subprocess import run
    from pathlib import Path
    _ = run(*p, cwd=Path(__file__).parent, **k,)
    if _.stdout: print(_.stdout)
    if _.stderr: print(_.stderr)
    return _

def build(commit=False):
    if commit:
        run('uvx hatchling version major')
        run('uv lock --upgrade-package json2rdf')
        run('git add -u') # https://github.com/pre-commit/pre-commit/issues/747#issuecomment-386782080
    run('uv build')


if __name__ == '__main__':
    from fire import Fire
    Fire({'build': build})
