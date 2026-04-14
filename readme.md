# pytest file validator

script to test the validity of 3 files (GTN.xlsx, Payrun.xlsx, mappings.json) according to the following 8 conditions:

1 - Files exist and are in proper format  
2 - GTN does not have line breaks between headers and data  
3 - GTN's header is on first row with no gaps  
4 - All employees in Payrun exist in GTN  
5 - All employees in GTN exist in Payrun  
6 - All pay elements outlined in mappings exist in Payrun  
7 - All pay elements outlined in mappings exist in GTN  
8 - All pay elements in GTN are of numeric type  

folders 1-8 have defective data designed to fail these tests, folder "proper" has normal data

# usage

copy test_task.py into the folder of your choosing and run pytest

# note

since I have not worked with pytest or unit testing before, I do not know some best practices, like for example on whether or not the tests should be in separate files. I found the one-file option to be more convenient so  variables can be used and the data doesn't get re-read a dozen times

might wanna run pytest with -x so that failure of one required condition doesn't cause cascading failures in others to clog up the output