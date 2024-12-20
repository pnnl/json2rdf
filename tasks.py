

def run(*p, **k):
    from subprocess import run
    from pathlib import Path
    _ = run(*p, cwd=Path(__file__).parent, **k,)
    if _.stdout: print(_.stdout)
    if _.stderr: print(_.stderr)
    return _

def build():
    run('uv lock --upgrade-package json2rdf')
    run('uvx hatchling version major')
    run('git add -u')
    run('uv build')


if __name__ == '__main__':
    build()