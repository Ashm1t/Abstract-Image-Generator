# Abstract Art Generator

Generate abstract art using style transfer and clustering. Fast generation (2-5 seconds) with 15 distinct styles.

## Setup

```bash
git clone https://github.com/yourusername/Abstract-Image-Generator.git
cd Abstract-Image-Generator
npm install
pip install pillow numpy torch torchvision
npm run dev
```

Open http://localhost:3000

## Styles

- Balanced Neutral: Clean compositions, medium contrast
- Warm Earth: Rich colors, organic textures
- Cool Flow: Fluid designs, cool palettes
- High Balance: Dynamic compositions
- Light Bright: Vibrant colors
- Cool Minimal: Clean, crisp designs
- High Drama: Bold contrasts
- Warm Texture: Rich textures
- Dark Mood: Deep compositions
- Warm Express: Energetic pieces
- Earth Ground: Natural compositions
- Bright Dynamic: High energy
- Subtle Mute: Sophisticated, muted
- Cool Structure: Architectural
- Dark Intense: Deep, intense

## Variations

- Blend: Combines similar artworks
- Filter: Enhances characteristics
- Color Morph: Transfers color palettes
- Cross-Style: Creates hybrids
- Mixed: Random combination

## Tech Stack

- Frontend: Next.js 13, Tailwind CSS
- Backend: Python, PIL, PyTorch
- Analysis: ResNet50, UMAP clustering
- Generation: Neural style transfer

## License

MIT
