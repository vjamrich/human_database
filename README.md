## Generating synthetic dataset of human images
We are living in an age when large datasets are becoming invaluable resource. Therefore, a power of being able to create data instead of collecting and manually labelling it further democratizes machine learning.

This project aims to provide a tool for generating a dataset containing hundreds of thousands synthetic human images, together with labels ranging from body proportions all the way to joint location, for machine learning purposes.

*Synthetic data definition*
>Any production data applicable to a given situation that are not obtained by direct measurement (McGraw-Hill, 2009)

*Why synthetic data generation?*
-	Cheaper to produce then collecting and labelling "real" data
-	To build software without exposing user data to developers *(such as PHI and PII)*
-	To meet specific conditions not available in real data


## Description
This program serves as a compatibility and automatization layer between various open-source programs, scripts, add-ons, CC0 databases and assets. To generate synthetic images of humans with various poses (motions performed), camera angles, clothing, and lighting conditions for machine learning purposes. Besides serving as a compatibility and automatization layer, it measures various parameters (see complete list of output [labels](Data/modifiers_dict.json)).

The output is generated in a form of images (exact format and other output parameters can be adjusted through settings GUI) and labels in <code>.csv</code> file format. The following preview shows 8 randomly generated images of humans:

![Synthetic human images](https://drive.google.com/uc?id=1F8hPmveLDuV2Cld5qNgCRC1Ibuotmw7K)

Settings can be adjusted to determine input and output file format, render engine used (rasterization or path tracing), output passes (depth maps, alpha maps, normal maps), and much more.

![Output setting GUI](https://drive.google.com/uc?id=1DREb8T5TopdkWWzKdFNFduEwgP0N1Y0h)


## Labels & Use cases
For all available output labels please see the following <code>.json</code> [file](Data/modifiers_dict.json).

Unless stated otherwise, the labels are in the 0-1 range. For example, the following preview shows age shifting from 0 to 1:

![Blending mesh based on the 'age' label output](https://drive.google.com/uc?id=1_bBFWVYAoADC5aNhfxDEhiu3ycWW4BoS)

The labels include, but are not limited to:

*Body proportions*
- For determining ideal clothing size of customers (improved targeting for promotional campaigns)
- <code>Height without shoes and hair [m]</code>
  <code>Neck circumference [m]</code>
  <code>Chest circumference [m]</code>
  <code>Muscle</code>
  <code>**+9 MORE**</code>

*Race*
- <code>African</code>
  <code>Asian</code>
  <code>Caucasian</code>


*Head shape*
- Finding ideal eyeglasses based on customers' head shape (targeting / promotional campaigns)
- <code>Head shape oval</code>
  <code>Head shape round</code>
  <code>Head shape rectangular</code>
  <code>**+4 MORE**</code>

*Ear shape*
- Determining ideal headphones / earphones
- <code>Ear (R) shape [0=Pointed, 1=Triangular]</code>
  <code>Ear (R) vertical position</code>
  <code>Ear (R) shape winged</code>
  <code>**+17 MORE**</code>

*Chin prognathism*
> Prognathism is a positional relationship of the mandible or maxilla to the skeletal base where either of the jaws protrudes beyond a predetermined imaginary line in the coronal plane of the skull
- <code>Chin prognathism [0=Maxillary, 0.5=Without, 1=Mandibular]</code>

*activity performed*
- <code>run</code>
  <code>walk</code>
  <code>other</code>

*Depth maps*
- Floating points between 0 and 1, where pixel with value 0 is closest to the camera while 1 furthest
- ![Depth maps output](https://drive.google.com/uc?id=1ZVuc2htG9JbTRFne_LmgW3Db4-quzW2M)
