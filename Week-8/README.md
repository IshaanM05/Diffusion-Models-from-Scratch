# Week 8 — Demo, Documentation, and Wrap-Up

> **Theme:** Make it usable by someone who isn't you.
> **Time commitment:** 8–12 hours
> **Deliverable due:** End of program (Friday EOD) — **Final demo day**

---

## What You'll Build

A **Gradio demo** wrapping the conditional DDPM/DDIM pipeline from Weeks 4-7, plus a short write-up and a presentation deck summarizing the eight weeks of work.

## Why This Week Matters

A model that only runs inside your own notebook isn't finished — it's just not yet shared. This week is entirely about packaging: making the work pushable, demoable, and explainable to someone who has zero context on diffusion models. It's also the only week explicitly about communication rather than new technical material.

## Deliverable Checklist

- [ ] Gradio interface: class selector, guidance scale slider, step count slider, seed input, Generate button (**compulsory**)
- [ ] Demo runs end-to-end from a clean Colab session
- [ ] Short technical write-up covering what was built and the biggest debugging challenges
- [ ] 5-slide presentation summarizing the program
- [ ] Final README pass across all eight week folders
- [ ] Everything pushed to GitHub

## Folder Structure

```
week8/
├── README.md
├── Week8_Assignment.ipynb
└── results/
    └── demo_screenshot.png
```

## Self-Check Questions

1. If a stranger cloned this repo and opened only the Week 8 notebook, could they generate a sample without reading anything else?
2. What's the one design decision from the past 8 weeks you'd undo if you started over?
3. What's the smallest change that would most improve sample quality right now?
4. What didn't make it into this program that you'd want to explore next (DPM-Solver, latent diffusion, text conditioning, etc.)?

## Common Pitfalls

- Gradio demo depends on a checkpoint file that isn't actually saved/loaded anywhere reproducible
- Forgetting to expose a seed control, making the demo non-reproducible for users reporting bugs
- Slider ranges that don't match what the model was actually trained/sampled with (e.g. allowing 1 step when the model needs at least ~10 to look like anything)
- A write-up that explains what the code does instead of why design decisions were made

**Quick links:**
- [Gradio docs](https://www.gradio.app/docs)
- [Hugging Face Spaces — deploying a Gradio app](https://huggingface.co/docs/hub/spaces-sdks-gradio)

---

**Program complete.** Eight weeks: PyTorch foundations → UNet → forward diffusion → DDPM → DDIM → conditional generation → custom dataset → demo.
