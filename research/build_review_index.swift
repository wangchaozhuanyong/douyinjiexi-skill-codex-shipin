import AppKit
import Foundation

enum ReviewIndexError: Error {
    case invalidArguments
    case noImages
    case cannotCreateBitmap
}

func aspectFit(_ source: NSSize, inside target: NSRect) -> NSRect {
    guard source.width > 0, source.height > 0 else { return target }
    let scale = min(target.width / source.width, target.height / source.height)
    let width = source.width * scale
    let height = source.height * scale
    return NSRect(
        x: target.midX - width / 2,
        y: target.midY - height / 2,
        width: width,
        height: height
    )
}

func buildIndex(
    reviewsRoot: URL,
    imageName: String,
    output: URL,
    columns: Int,
    rows: Int,
    cellWidth: Int,
    cellHeight: Int
) throws {
    let fileManager = FileManager.default
    let directories = try fileManager.contentsOfDirectory(
        at: reviewsRoot,
        includingPropertiesForKeys: [.isDirectoryKey],
        options: [.skipsHiddenFiles]
    ).filter {
        (try? $0.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) == true
            && fileManager.fileExists(atPath: $0.appendingPathComponent(imageName).path)
    }.sorted { $0.lastPathComponent < $1.lastPathComponent }

    guard !directories.isEmpty else { throw ReviewIndexError.noImages }
    let canvasWidth = columns * cellWidth
    let canvasHeight = rows * cellHeight
    guard let bitmap = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: canvasWidth,
        pixelsHigh: canvasHeight,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    ) else {
        throw ReviewIndexError.cannotCreateBitmap
    }

    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    NSColor(calibratedRed: 0.04, green: 0.05, blue: 0.06, alpha: 1).setFill()
    NSRect(x: 0, y: 0, width: canvasWidth, height: canvasHeight).fill()

    let titleStyle: [NSAttributedString.Key: Any] = [
        .font: NSFont.monospacedSystemFont(ofSize: 18, weight: .semibold),
        .foregroundColor: NSColor.white,
    ]

    for (index, directory) in directories.prefix(columns * rows).enumerated() {
        guard let image = NSImage(contentsOf: directory.appendingPathComponent(imageName)) else {
            continue
        }
        let column = index % columns
        let rowFromTop = index / columns
        let originX = column * cellWidth
        let originY = canvasHeight - (rowFromTop + 1) * cellHeight
        let cell = NSRect(
            x: originX + 8,
            y: originY + 8,
            width: cellWidth - 16,
            height: cellHeight - 16
        )
        NSColor(calibratedRed: 0.08, green: 0.09, blue: 0.11, alpha: 1).setFill()
        cell.fill()
        let titleRect = NSRect(
            x: cell.minX + 10,
            y: cell.maxY - 32,
            width: cell.width - 20,
            height: 24
        )
        directory.lastPathComponent.draw(in: titleRect, withAttributes: titleStyle)
        let imageArea = NSRect(
            x: cell.minX + 8,
            y: cell.minY + 8,
            width: cell.width - 16,
            height: cell.height - 48
        )
        image.draw(
            in: aspectFit(image.size, inside: imageArea),
            from: NSRect(origin: .zero, size: image.size),
            operation: .sourceOver,
            fraction: 1
        )
    }
    NSGraphicsContext.restoreGraphicsState()

    if let data = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.9]) {
        try data.write(to: output)
    }
}

guard CommandLine.arguments.count == 8 else {
    throw ReviewIndexError.invalidArguments
}

try buildIndex(
    reviewsRoot: URL(fileURLWithPath: CommandLine.arguments[1]),
    imageName: CommandLine.arguments[2],
    output: URL(fileURLWithPath: CommandLine.arguments[3]),
    columns: Int(CommandLine.arguments[4]) ?? 3,
    rows: Int(CommandLine.arguments[5]) ?? 6,
    cellWidth: Int(CommandLine.arguments[6]) ?? 640,
    cellHeight: Int(CommandLine.arguments[7]) ?? 520
)
