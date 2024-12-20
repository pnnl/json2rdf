

def run(*p, **k):
    from subprocess import run
    from pathlib import Path
    return run(*p, cwd=Path(__file__.parent), **k)

def build():
    run('uvx hatchling version major') 
    run('git add uv.lock')
    run('uv build')


if __name__ == '__main__':
    build()