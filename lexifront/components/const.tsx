import logoUrl from "../assets/logo.png";

export function Prettybackground() {
  const colours: number[][] = [
    [10, 10, 13],
    [13, 10, 10],
    [10, 13, 10],
    [10, 10, 10],
  ];
  const patterns: number[][][] = [];
  const size: number = 50;
  const count: number = 10;

  for (let i: number = 0; i < count; i++) {
    const pattern: number[][] = [];
    for (let y: number = 0; y < size; y++) {
      const row: number[] = [];
      for (let x: number = 0; x < size; x++) {
        row.push(Math.floor(Math.random() * colours.length));
      }
      pattern.push(row);
    }
    patterns.push(pattern);
  }

  const screenWidth = typeof window !== "undefined" ? window.innerWidth : 1920;
  const screenHeight =
    typeof window !== "undefined" ? window.innerHeight : 1080;
  const modifier = 10000 as number
  const tilesX = Math.ceil(screenWidth / (size*modifier));
  const tilesY = Math.ceil(screenHeight / (size*modifier));

  const bigCanvas = document.createElement("canvas");
  bigCanvas.width = tilesX * size;
  bigCanvas.height = tilesY * size;
  const bigCtx = bigCanvas.getContext("2d");

  if (bigCtx) {
    for (let ty: number = 0; ty < tilesY; ty++) {
      for (let tx: number = 0; tx < tilesX; tx++) {
        const pattern = patterns[Math.floor(Math.random() * patterns.length)];
        for (let y: number = 0; y < size; y++) {
          for (let x: number = 0; x < size; x++) {
            const colorIndex = pattern[y][x];
            const color = colours[colorIndex];
            bigCtx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
            bigCtx.fillRect(tx * size + x, ty * size + y, 1, 1);
          }
        }
      }
    }
  }

  const backgroundImage = bigCanvas.toDataURL();
  const canvasWidth = tilesX * size;
  const canvasHeight = tilesY * size;

  return (
    <div
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundRepeat: "repeat",
        // imageRendering: "pixelated",
        zIndex:"-1",
        minHeight: "100vh",
        minWidth:"100vw",
        position: "absolute",
      }}
    >
 
    </div>
  );
}

export function Content({ children }: { children: React.ReactNode }) {
  return (
    <div id="page-container">
      <div
        id="page-content"
        style={
          {
            // padding: 20,
            // paddingBottom: 50,
            // minHeight: "100vh",
          }
        }
      >
        {children}
      </div>
    </div>
  );
}

export function Logo() {
  return (
    <div
      style={{
        marginTop: 20,
        marginBottom: 10,
      }}
    >
      <a href="/">
        <img src={logoUrl} height={64} width={64} alt="logo" />
      </a>
    </div>
  );
}


