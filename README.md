# Image Tools

## Requirements

```bash
pip install Pillow
```

## im_compress.py

Compress images to a target file size.

```bash
python3 im_compress.py photo.jpg -s 200           # compress to 200KB
python3 im_compress.py ./photos -s 100 -o ./out   # batch compress folder
```

## jpg2pdf.py

Convert images to PDF or merge multiple images into one PDF.

```bash
python3 jpg2pdf.py image.jpg                 # single image to PDF
python3 jpg2pdf.py ./scans -o combined.pdf   # merge folder to PDF
```

## avatar_gen.py

Generate circular avatar images with centered text.

```bash
python3 avatar_gen.py A "#000000" --out google_ng.png
```

gen_avatar does not make an exact copy of google letters
