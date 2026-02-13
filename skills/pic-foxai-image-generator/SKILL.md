---
name: pic-foxai-image-generator
description: "Automate generating images on pic.foxai.edu.kg (FoxAI PIC) via the web UI: log in with access code 20200108, set prompt/negative prompt, choose text-to-image model, set resolution (width/height) and output count, click generate, then download the resulting image(s) (single image or ZIP). Use when the user asks to generate images specifically through pic.foxai.edu.kg instead of local SD/ComfyUI, or when they provide model/resolution/count constraints for that site."
---

# pic.foxai.edu.kg Image Generator

## Workflow

Automate the site end-to-end with the Playwright MCP tools:
1) open the site, 2) log in (if prompted), 3) set prompt + parameters, 4) generate, 5) download, 6) return the downloaded file paths (and extract ZIP when needed).

### Inputs To Collect From The User

- `prompt` (required): positive prompt.
- `negative_prompt` (optional).
- `model` (optional): a name/alias; default to `FLUX.1 [schnell]` if not specified.
- `resolution` (optional): either `WIDTHxHEIGHT` (preferred) or a descriptor like `square`, `portrait`, `landscape`. Default `1024x1024`.
- `count` (optional): `1..8`, default `1`.

If the user provides only a “prompt”, keep defaults and proceed.

### Model Selection Heuristics

Map common user aliases to the site’s model dropdown labels:
- `flux`, `schnell`, `default` -> `FLUX.1 [schnell]`
- `sdxl` -> `Stable Diffusion XL Base 1.0`
- `dreamshaper` -> `DreamShaper 8 LCM`
- `lightning` -> `Stable Diffusion XL Lightning`
- `img2img` -> `Stable Diffusion v1.5 图生图` (requires image URL on the page)
- `inpaint`, `局部重绘` -> `Stable Diffusion v1.5 局部重绘` (requires image URL, optional mask URL)

If the user requests `img2img`/`inpaint` but does not provide URLs, ask for the required URL(s) before generating.

### Resolution Heuristics

- If the user gives `WIDTHxHEIGHT`, set width/height exactly.
- If the user says `square`: use `1024x1024`.
- If `portrait`: use `832x1216` (or any site-supported portrait pair; adjust if sliders reject).
- If `landscape`: use `1216x832` (same note).

### Step 1: Navigate And Log In (Access Code 20200108)

Use Playwright MCP tools (preferred), and treat the login modal as conditional.

Use this snippet via `mcp__playwright__browser_run_code` to ensure you are logged in:

```js
async (page) => {
  await page.goto('https://pic.foxai.edu.kg/', { waitUntil: 'domcontentloaded' });

  // Login modal appears as: heading "请输入访问密码", textbox "访问密码", button "登录".
  const modalHeading = page.getByRole('heading', { name: '请输入访问密码' });
  const isModalVisible = await modalHeading.isVisible().catch(() => false);
  if (isModalVisible) {
    await page.getByRole('textbox', { name: '访问密码', exact: true }).fill('20200108');
    await page.getByRole('button', { name: '登录' }).click();
    await modalHeading.waitFor({ state: 'hidden', timeout: 15000 });
  }
}
```

### Step 2: Set Prompt, Model, Count, Resolution

1. Fill prompt boxes:
   - Positive prompt textbox role/name contains `正向提示词`.
   - Negative prompt textbox role/name contains `反向提示词`.
2. Select model:
   - Combobox role/name contains `文生图模型`.
3. Select count:
   - Combobox role/name contains `生成数量` (options `1..8`).
4. Set width/height:
   - Click `高级选项` “显示/隐藏” if sliders are not visible.
   - Sliders role/name contain `图像宽度` and `图像高度`.

This snippet sets everything deterministically:

```js
async (page, args) => {
  const {
    prompt,
    negativePrompt = '',
    modelLabelRegex = /FLUX\\.1 \\[schnell\\]/,
    count = 1,
    width = 1024,
    height = 1024,
  } = args;

  await page.getByRole('textbox', { name: /正向提示词/ }).fill(prompt);
  await page.getByRole('textbox', { name: /反向提示词/ }).fill(negativePrompt);

  await page.getByRole('combobox', { name: /文生图模型/ }).selectOption({ label: modelLabelRegex });
  await page.getByRole('combobox', { name: /生成数量/ }).selectOption(String(count));

  // Ensure advanced options are expanded (sliders are only visible then).
  const widthSlider = page.getByRole('slider', { name: /图像宽度/ });
  const widthVisible = await widthSlider.isVisible().catch(() => false);
  if (!widthVisible) {
    await page.getByRole('button', { name: /显示\\/隐藏/ }).click();
    await widthSlider.waitFor({ state: 'visible', timeout: 5000 });
  }

  // Set range inputs precisely + trigger input/change so UI updates.
  const setSlider = async (slider, value) => {
    await slider.evaluate((el, v) => {
      el.value = String(v);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    }, value);
  };

  await setSlider(page.getByRole('slider', { name: /图像宽度/ }), width);
  await setSlider(page.getByRole('slider', { name: /图像高度/ }), height);
}
```

### Step 3: Generate

Click `生成图像` and wait until the result shows `生成成功`:

```js
async (page) => {
  await page.getByRole('button', { name: /生成图像/ }).click();
  await page.getByText(/生成成功/).first().waitFor({ timeout: 60000 });
}
```

### Step 4: Download (Single Image Or ZIP)

- If `count === 1`: click `下载图像`.
- If `count > 1`: click `下载ZIP` (preferred) and extract it.

Use this snippet to download to an absolute path:

```js
async (page, args) => {
  const { outPath, zip } = args;
  const buttonName = zip ? /下载ZIP/ : /下载图像/;

  const [download] = await Promise.all([
    page.waitForEvent('download', { timeout: 30000 }),
    page.getByRole('button', { name: buttonName }).click(),
  ]);

  await download.saveAs(outPath);
  return { outPath, suggested: download.suggestedFilename() };
}
```

If you downloaded a ZIP, extract via shell:

```bash
unzip -o /path/to/download.zip -d /path/to/outdir
```

## Notes

- The site UI includes icon glyphs in accessible names; match on the Chinese text with regex (e.g. `/下载图像/`) instead of exact full labels.
- The login modal may not appear if already authenticated; always handle it conditionally.

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
