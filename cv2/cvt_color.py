import numpy as np
import cv2


def color2gray(img, convertor, weight=[1, 1, 1]):
    """
    把彩色图像按照指定的权重转换为灰度图像

    可以在把彩色图像转换为灰度图像时，使某种颜色突出

    权重向量不为0

    Args:
        img: 彩色图像，3通道图像

        convertor: 转换器
            "3c2gray": RGB/BRG 3通道转换为灰度图像
            "hsv2gray": HSV 3通道转换为灰度图像

        weight: 权重向量，3-element list

    Returns:
        灰度图像，单通道图像
    """

    assert len(weight) == 3, "Weight must be a 3-element list"
    assert sum(weight) != 0, "Weight must not be all zeros"
    assert len(img.shape) == 3, "Input image must be a 3D array"
    assert convertor in [
        "3c2gray",
        "hsv2gray",
    ], f"Convertor {convertor} is not supported"

    # 标准化权重向量，使其模为1，这样可以使在输出的灰度图像中，完全符合权重向量的颜色为白色
    normalise = lambda W: W / np.sqrt(np.sum(W**2))
    # 不同的转换器对应的标准颜色
    std_color = (
        np.array([255, 255, 255])
        if convertor == "3c2gray"
        else np.array([180, 255, 255])
    )

    normalised_weight = normalise(np.array(weight))
    norm_img = img / np.sqrt(np.sum(std_color**2))
    gray_img = np.dot(norm_img, normalised_weight)
    gray_img = (gray_img * 255).astype(np.uint8)
    return gray_img


if __name__ == "__main__":
    img = cv2.imread("_aaa.jpg")
    gray_img = color2gray(img, convertor="3c2gray")
    cv2.imwrite("gray_image.jpg", gray_img)
