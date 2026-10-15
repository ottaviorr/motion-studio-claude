// Confere a transparência de um .mov HEVC com alfa (o ffmpeg não decodifica o alfa do HEVC; o AVFoundation sim).
// swiftc -O alfa.swift -o alfa && ./alfa arquivo.mov segundo saida.png   → imprime o alfa de 3 pontos e salva o quadro em PNG
import AVFoundation
import AppKit
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let g = AVAssetImageGenerator(asset: AVURLAsset(url: url))
g.requestedTimeToleranceBefore = .zero; g.requestedTimeToleranceAfter = .zero
let img = try! g.copyCGImage(at: CMTime(seconds: Double(CommandLine.arguments[2])!, preferredTimescale: 600), actualTime: nil)
let rep = NSBitmapImageRep(cgImage: img)
for (x,y) in [(10,10),(1800,1000),(300,500)] { let c = rep.colorAt(x: x, y: y)!; print(x,y,"alfa", c.alphaComponent) }
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[3]))
