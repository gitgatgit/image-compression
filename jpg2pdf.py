#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image

def load_image(path: Path) -> Image.Image:
    img = Image.open(path)
    if img.mode in ("RGBA", "LA"):
        img = img.convert("RGB")
    return img

def single_to_pdf(input_file: Path, output_file: Path):
    img = load_image(input_file)
    img.save(output_file, "PDF", resolution=300.0)
    print(f"✅ Saved {output_file}")

def merge_all(directory: Path, output_file: Path):
    files = sorted(
        list(directory.glob("*.jpg")) +
        list(directory.glob("*.jpeg")) +
        list(directory.glob("*.png"))
    )

    if not files:
        raise RuntimeError("No JPG/JPEG/PNG files found")

    images = [load_image(p) for p in files]

    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        resolution=300.0
    )
    print(f"✅ Merged {len(images)} images into {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert JPGs to PDF")
    parser.add_argument("path", help="JPG file or directory")
    parser.add_argument("-o", "--output", help="Output PDF file")

    args = parser.parse_args()
    path = Path(args.path)

    if path.is_file():
        output = Path(args.output) if args.output else path.with_suffix(".pdf")
        single_to_pdf(path, output)

    elif path.is_dir():
        output = Path(args.output) if args.output else path / "merged.pdf"
        merge_all(path, output)

    else:
        raise RuntimeError("Invalid path")

if __name__ == "__main__":
    main()
