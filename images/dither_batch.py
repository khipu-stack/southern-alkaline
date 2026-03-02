from pathlib import Path

from PIL import Image


def process_image(
    input_path: Path,
    output_path: Path,
    target_width: int = 1000,
    temp_width: int = 250,
    palette_size: int = 16,
) -> None:
    with Image.open(input_path) as img:
        src = img.convert("RGB")
        src_width, src_height = src.size
        temp_height = round(src_height * (temp_width / src_width))
        target_height = round(src_height * (target_width / src_width))

        reduced = src.resize((temp_width, temp_height), Image.Resampling.LANCZOS)
        dithered = reduced.quantize(
            colors=palette_size,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        chunky = dithered.resize((target_width, target_height), Image.Resampling.NEAREST)
        chunky.save(output_path, format="PNG", optimize=True, compress_level=9)


def main() -> None:
    base = Path(".")
    inputs = {
        1: base / "vn1.jpeg",
        2: base / "vn2.jpg",
        3: base / "vn3.jpg",
        4: base / "vn4.jpg",
    }
    for i, input_path in inputs.items():
        output_path = base / f"vn_underground_color_{i}.png"

        if not input_path.exists():
            print(f"SKIP: {input_path} not found")
            continue

        process_image(input_path, output_path)
        print(f"OK: {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
