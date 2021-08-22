import PIL
from PIL import Image, ImageTk


def mergeImages(baseImage: Image, overlay: Image, offset: tuple[int, int]) -> PIL.Image:
    """ doesn't modify the input images, returns a new merged (unscaled) image """
    overlayPixels = overlay.load()

    mergedPicture = baseImage.copy()
    mergedPixels = mergedPicture.load()

    for xPixel in range(0, overlay.size[0]):
        for yPixel in range(0, overlay.size[1]):
            targetX = xPixel + offset[0]
            targetY = yPixel + offset[1]

            if targetX < 0 or targetX >= baseImage.size[0]:
                continue
            if targetY < 0 or targetY >= baseImage.size[1]:
                continue

            overlayPixel = overlayPixels[xPixel, yPixel]
            if len(overlayPixel) == 4 and overlayPixel[3] < 250:
                # skip transparent pixels
                continue
            mergedPixels[targetX, targetY] = overlayPixel

    return mergedPicture


def createResultImage(image: Image, mask: Image):
    """ Does not modify the input images, creates a new copy which is returned """
    outputImage = Image.new("RGB", image.size, (200, 200, 200))

    if image.size != mask.size:
        print("[ERROR] invalid mask size!")
        return outputImage

    filterColours = [(255, 0, 255, 255), (255, 0, 0, 255),  # with alpha channel
                     (255, 0, 255), (255, 0, 0)]  # without alpha channel

    imagePixels = image.load()
    maskPixels = mask.load()
    outputPixels = outputImage.load()

    for xPixel in range(0, image.size[0]):
        for yPixel in range(0, image.size[1]):
            maskPixel = maskPixels[xPixel, yPixel]
            if maskPixel not in filterColours:
                outputPixels[xPixel, yPixel] = imagePixels[xPixel, yPixel]
            else:
                pass
    return outputImage


def generateDeltaMask(image: Image, modifiedImage: Image, shadow: Image) -> Image:
    newShadow = shadow.copy()
    imagePixels = image.load()
    modifiedImagePixels = modifiedImage.load()
    newShadowPixels = newShadow.load()

    for xPixel in range(0, image.size[0]):
        for yPixel in range(0, image.size[1]):
            if modifiedImagePixels[xPixel, yPixel] != imagePixels[xPixel, yPixel]:
                newShadowPixels[xPixel, yPixel] = (255, 255, 255)

    return newShadow
