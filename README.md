# IGE - Instagram Empire

<h2>Summary</h2>
The ultimate goal of IGE is to create an automated system for running a multitude of Instagram accounts.
This project aims to build a system that requires minimal input from the user while being able to manage up to 150 Instagram accounts, all posting daily content based on different topics and niches.

Once the system is capable of running many accounts, work can begin on analytics and finding marketing opportunities. As there will be many pages with (hopefully) many followers, I open up a variety of markets that could potentially be interesting to advertisers or sponsors. Past that, there is only perfecting the system and selling it off, however, I'll be lucky if I manage to get even one advertiser on board.

<br>

<h2>Outline</h2>
There are several basic milestones to reach for within a handful of categories:
<ol>

    <li><h3>Management</h3>
        <ul>
            <li>A custom web application will be built to give an interactive view of the entire system. </li>
            <li>It will let me manage each profile separately, see its analytics, manually post and comment, change which parts of the database it can pull images from etc.</li>
            <li>The application will also allow me to browse my database of images with extra information regarding my content. Info such as how many images are ready to post, specific image category shortages, etc </li>
        </ul>
    </li>

    <li><h3>Content</h3>
        <ul>
            <li>I have thousands of collected screenshots ready to be parsed and added to a database.</li>
            <li>Thousands more images are bookmarked on my personal Instagram for future retreival.</li>
            <li>Another system will be built to be able to browse hundreds of pages based on topics. For instance, there will be separate home feeds for dogs, cars, architecture, etc that I can acquire images from </li>
        </ul>
    </li>
    
    <li><h3>Posting</h3>
        <ul>
            <li>The posting will happen automatically at a randomly generated time within a certain time frame of the day. </li>
            <li>Pages will be sorted into 3 categories:
                <ol>
                <li><b>Properly sourced, manual caption</b> - Images where I can tag the original poster to give them credit. This will have a bonus of manually written captions to ensure quality uploads</li>
                <li><b>Properly sourced, auto-caption</b> - Similar to the above but for ease of operation, not all pages will have manual caption. Some will simply tag the source and add the hashtags.</li>
                <li><b>Unsourced, auto-caption</b> - These are images for which I can't give credit. These profiles will essentially be a dump of the random images I have with captions auto picked from a list of generic captions.</li>

                </ol>        
            </li>
            <li>Possibilty of voice-to-text manual caption entry for ease of use and speed.</li>
        </ul>
    </li>
    
    <li><h3>Interaction</h3>
        <ul>
            <li>Make crawlers to collect lists of instagram users potentially interested in one of my specific pages. Lists will come from the followers of other pages, as well as users that comment and like certain posts related to my page.</li>
            <li>My profiles will also be able to like and comment on other users' content. The liking can be simple random liking but the comments will require manual creation of a list of generic comments. The goal is to press one button, pick a comment category and it leaves a comment. This is in place of actually typing out a full personal comment.</li>            
        </ul>
    </li>    
</ol>
<br>
Achieving these objectives is not as simple as it seems though. Several languages are required and the project relies on existing libraries. However, once all these ideas are realized and implemented, the system should be able to run smoothly.


<br><br>
<h4>UPDATE: March 1st, 2017<h/4>

<h2>Image Processing - Parsing the Screenshots</h2>
In order to seed the Instagram profile with an initial amount of photos, hundreds of screenshots were collected for various interests.The screenshots contain a profile name followed by the image that the profile posted. I am interested in just those two pieces of data.

I have written a Python script that will parse the image and retrieve both the name (in text format) and a cropped version of the image.
The name is obtained by first blurring the entire screenshot in order to "spread" the darker pixels, the text in particular.
After blurring, the image undergoes a thresholding where pixels whose value is above a certain threshold are white and pixels below or equal to that value are black. This will give us a true, binary black and white image with groups of black pixels on a white background.

After repeating the process of blurring and thresholding one more time, the blurred text can easily be identified as one single blob. To do this, I set parameters that look at the size and position of each blob in the image. Once there is a match for my parameters, I grow the area of the blob outward by several pixels, as to not run into edge problems, and then using the coordinates of the blob, I crop the original screenshot. This leaves me with a PNG image of the profile name text.

Optionally, I have the choice of retrieving the image from the sreenshot as well. The image is obtained by simply finding the biggest blob of pixels. This will work on all images except those that have a large white pixel count. The problem occurs most notably for things like Twitter screenshots and quotes on a white background as the algorithm that groups pixels into blobs relies on them being dark.

