import argparse
import time
from PIL import Image

def mov_avg_half(in_pix, w, h, r):
    size = w * h
    out_pix = [None] * size
    kernel = 2 * r + 1

    for i in range(h):
        rd, gr, bl = 0, 0, 0
        f = i * w
        
        for k_ver in range(f, min(f + r + 1, f + w)):
            rd += in_pix[k_ver][0]
            gr += in_pix[k_ver][1]
            bl += in_pix[k_ver][2]
        
        p = 0
        for j in range(w):
            add = min(f + j + r, f + w - 1)
            
            if j == 0:
                out_pix[f + j] = (rd // (r + 1), gr // (r + 1), bl // (r + 1))
            else:
                if p < r:
                    rd += in_pix[add][0]
                    gr += in_pix[add][1]
                    bl += in_pix[add][2]
                    p += 1
                    d = (r + 1) + p
                    out_pix[f + j] = (rd // d, gr // d, bl // d)
                else:
                    rd += in_pix[add][0] - in_pix[f + j - r - 1][0]
                    gr += in_pix[add][1] - in_pix[f + j - r - 1][1]
                    bl += in_pix[add][2] - in_pix[f + j - r - 1][2]
                    out_pix[f + j] = (rd // kernel, gr // kernel, bl // kernel)
    
    return out_pix

def mov_avg(in_pix, w, h, r):
    tmp = mov_avg_half(in_pix, w, h, r)
    return mov_avg_half(tmp, h, w, r)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to save the output image")
    parser.add_argument("radius", type=int, help="Blur radius")
    parser.add_argument("scale", type=float, help="Scaling factor")
    args = parser.parse_args()
    
    start_time = time.time()
    
    image = Image.open(args.input).convert("RGB")
    
    if args.scale != 1:
        new_size = (int(image.width / args.scale), int(image.height / args.scale))
        image = image.resize(new_size, Image.LANCZOS)
    
    w, h = image.size
    in_pix = list(image.getdata())
    
    out_pix = mov_avg(in_pix, w, h, args.radius)
    
    out_image = Image.new("RGB", (w, h))
    out_image.putdata(out_pix)
    out_image.save(args.output)
    
    end_time = time.time()
    print(f"Processing time: {end_time - start_time:.4f} seconds")
    
if __name__ == "__main__":
    main()
