

def get_rev():
    from subprocess import check_output as run
    return run('git rev-parse --abbrev-ref HEAD', text=True).strip()
rev = get_rev()


def build(commit=False):
    def run(cmd, *p, **k):
        from subprocess import check_call as run
        from pathlib import Path
        return run(cmd, *p, cwd=Path(__file__).parent, **k)
    if commit:
        run(f'uvx hatchling version {ncommits()+1}', )
        run('uv lock --upgrade-package json2rdf', )
        # https://github.com/pre-commit/pre-commit/issues/747#issuecomment-386782080
        run('git add -u', )
    run('uv build')


def ncommits(rev=rev):
    from subprocess import check_output as run
    c = run(f'git rev-list --count {rev}', text=True).strip()
    return int(c)


def chk_ver(rev=rev):
    from json2rdf import __version__ as v
    return str(v) == str(ncommits(rev=rev))


if __name__ == '__main__':
    from fire import Fire
    Fire({f.__name__:f for f in {build, chk_ver}})
