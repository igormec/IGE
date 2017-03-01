# IGE - Instagram Empire

The ultimate goal of IGE is to create an automated system for running a multitude of Instagram accounts.
This project aims to build a system that requires minimal input from the user while being able to manage up to 150 Instagram accounts, all posting daily content based on different topics and niches. Once the system is capable of running many accounts, work can begin on analytics and finding marketing opportunities. As there will be many pages with (hopefully) many followers, I open up a variety of markets that could potentially be interesting to advertisers or sponsors. Past that, there is only perfecting the system and selling it off, however, I'll be lucky if I manage to get even one advertiser on board.







UPDATE: March 1st, 2017

In order to seed the Instagram profile with an initial amount of photos, hundreds of screenshots were collected for various interests.The screenshots contain a profile name followed by the image that the profile posted. I am interested in just those two pieces of data.

<h2>Image Processing</h2>

I have written a Python script that will parse the image and retrieve both the name (in text format) and a cropped version of the image.
The name is obtained by first blurring the entire screenshot in order to "spread" the darker pixels, the text in particular.
After blurring, the image undergoes a thresholding where pixels whose value is above a certain threshold are white and pixels below or equal to that value are black. This will give us a true, binary black and white image with groups of black pixels on a white background.

After repeating the process of blurring and thresholding one more time, the blurred text can easily be identified as one single blob. To do this, I set parameters that look at the size and position of each blob in the image. Once there is a match for my parameters, I grow the area of the blob outward by several pixels, as to not run into edge problems, and then using the coordinates of the blob, I crop the original screenshot. This leaves me with a PNG image of the profile name text.

Optionally, I have the choice of retrieving the image from the sreenshot as well. The image is obtained by simply finding the biggest blob of pixels. This will work on all images except those that have a large white pixel count. The problem occurs most notably for things like Twitter screenshots and quotes on a white background as the algorithm that groups pixels into blobs relies on them being dark.

