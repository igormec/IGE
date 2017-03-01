# IGE
Automated system for running multiple Instagram accounts


UPDATE: March 1st, 2017

In order to seed the Instagram profile with an initial amount of photos, hundreds of screenshots were collected for various interests.The screenshots contain a profile name followed by the image that the profile posted. I am interested in just those two pieces of data.

<h2>Image Processing</h2>

I have written a Python script that will parse the image and retrieve both the name (in text format) and a cropped version of the image.
The name is obtained by first blurring the entire screenshot in order to "spread" the darker pixels, the text in particular.
After blurring, the image undergoes a thresholding where pixels whose value is above a certain threshold are white and pixels below or equal to that value are black. This will give us a true, binary black and white image with groups of black pixels on a white background.

After repeating the process of blurring and thresholding one more time, the blurred text can easily be identified as one single blob. To do this, I set parameters that look at the size and position of each blob in the image. Once there is a match for my parameters, I grow the area of the blob outward by several pixels, as to not run into edge problems, and then using the coordinates of the blob, I crop the original screenshot. This leaves me with a PNG image of the profile name text.

Optionally, I have the choice of retrieving the image from the sreenshot as well. The image is obtained by simply finding the biggest blob of pixels. This will work on all images except those that have a large white pixel count. The problem occurs most notably for things like Twitter screenshots and quotes on a white background as the algorithm that groups pixels into blobs relies on them being dark.

