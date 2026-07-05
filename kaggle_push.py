"""
Push all 8 diffusion notebooks to Kaggle as private GPU kernels.
Credentials are injected in-memory only — never written to the repo notebooks.
"""

import json, os, shutil, subprocess, sys, tempfile, pathlib, time

KAGGLE_USERNAME = "ishaanmondal"
WANDB_API_KEY   = os.environ.get("WANDB_API_KEY", "")
HF_TOKEN        = os.environ.get("HF_TOKEN",       "")
HF_USERNAME     = os.environ.get("HF_USERNAME",    "IshaanM05")

REPO_DIR = pathlib.Path(__file__).parent

# (week, notebook path, slug, title-that-generates-that-slug)
NOTEBOOKS = [
    (1, "Week-1/Week1_Assignment.ipynb", "diffusion-week-1",              "Diffusion Week 1"),
    (2, "Week-2/Week2_Assignment.ipynb", "diffusion-week-2",              "Diffusion Week 2"),
    (3, "Week-3/Week3_Assignment.ipynb", "diffusion-wk3-forward-diffusion", "Diffusion Wk3 Forward Diffusion"),
    (4, "Week-4/Week4_Assignment.ipynb", "diffusion-wk4-ddpm-training",    "Diffusion Wk4 DDPM Training"),
    (5, "Week-5/Week5_Assignment.ipynb", "diffusion-wk5-ddim-sampling",    "Diffusion Wk5 DDIM Sampling"),
    (6, "Week-6/Week6_Assignment.ipynb", "diffusion-wk6-cfg-conditional",  "Diffusion Wk6 CFG Conditional"),
    (7, "Week-7/Week7_Assignment.ipynb", "diffusion-wk7-butterflies-dataset", "Diffusion Wk7 Butterflies Dataset"),
    (8, "Week-8/Week8_Assignment.ipynb", "diffusion-wk8-demo-deployment",  "Diffusion Wk8 Demo Deployment"),
]

CREDS_CELL = {
    "cell_type": "code",
    "id": "creds-inject",
    "metadata": {},
    "outputs": [],
    "source": [
        "import os\n",
        f'os.environ["WANDB_API_KEY"] = "{WANDB_API_KEY}"\n',
        f'os.environ["HF_TOKEN"] = "{HF_TOKEN}"\n',
        f'os.environ["HF_USERNAME"] = "{HF_USERNAME}"\n',
        'print("Credentials set.")\n',
    ]
}


def make_metadata(week, slug, title, nb_filename):
    return {
        "id": f"{KAGGLE_USERNAME}/{slug}",
        "title": title,
        "code_file": nb_filename,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_tpu": False,
        "enable_internet": True,
        "run_on_save": True,
        "dataset_sources": [],
        "competition_sources": [],
        "kernel_sources": [],
    }


def push(week, nb_rel_path, slug, title):
    nb_path = REPO_DIR / nb_rel_path
    nb_filename = nb_path.name

    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)

    # Inject credentials cell after first cell (setup / imports) for weeks that need credentials
    if week in (7, 8):
        nb["cells"].insert(1, CREDS_CELL)

    tmp_dir = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp_dir / nb_filename).write_text(json.dumps(nb, indent=1), encoding="utf-8")
        (tmp_dir / "kernel-metadata.json").write_text(
            json.dumps(make_metadata(week, slug, title, nb_filename), indent=2)
        )

        result = subprocess.run(
            ["kaggle", "kernels", "push", "-p", str(tmp_dir)],
            capture_output=True, text=True
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    url = f"https://www.kaggle.com/code/{KAGGLE_USERNAME}/{slug}"
    if result.returncode == 0:
        print(f"  [OK ] Week {week} — {url}")
    else:
        print(f"  [ERR] Week {week}:")
        print("       ", (result.stdout + result.stderr).strip().replace("\n", "\n        "))
    return result.returncode == 0


def status():
    from kaggle import KaggleApi
    api = KaggleApi()
    api.authenticate()
    print("Status of all kernels:")
    for week, _, slug, *_ in NOTEBOOKS:
        try:
            s = api.kernels_status(f"{KAGGLE_USERNAME}/{slug}")
            import json as _json
            d = _json.loads(str(s))
            state = d.get("status", "?")
            fail  = d.get("failureMessage") or ""
            line  = f"{state}{(' — ' + fail[:80]) if fail else ''}"
        except Exception as e:
            line = f"(API error: {str(e)[:60]})"
        print(f"  Week {week} [{slug}]: {line}")


if __name__ == "__main__":
    try:
        import kaggle  # noqa: F401
    except ImportError:
        print("Installing kaggle package...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kaggle"], check=True)

    if "--status" in sys.argv:
        status()
        sys.exit(0)

    print("Pushing all 8 notebooks to Kaggle (private, GPU + internet, run_on_save)...\n")
    results = []
    for week, path, slug, title in NOTEBOOKS:
        results.append(push(week, path, slug, title))

    ok = sum(results)
    print(f"\n{ok}/{len(NOTEBOOKS)} submitted successfully.")
    if ok > 0:
        print("\nCheck progress any time:  python kaggle_push.py --status")
