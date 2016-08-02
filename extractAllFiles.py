'''
Information taken from https://github.com/libyal/libewf/wiki/Development
http://www.sleuthkit.org/sleuthkit/docs/api-docs/4.3/
https://github.com/py4n6/pytsk/blob/master/examples/fls.py
https://github.com/py4n6/pytsk/wiki - Listing all files in a directory

'''
#!/usr/bin/env python
import sys, time, os, re
import pytsk3
import pyewf
import extractSystemInfo

counter = 1

class ewf_Img_Info(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_Img_Info, self).__init__(url = '', type = pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()
        
    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)
    
    def get_size(self):
        return self._ewf_handle.get_media_size()
        
'''
find all files in an image. If the file is a folder get in the folder and find all files and folders, etc. recursively

parts taken from example in https://github.com/py4n6/pytsk/blob/master/examples/fls.py

The directory is a TSK_FS_DIR struct that has: addr, names, fs_file (pointer to the file structure), fs_info (pointer to the file system the dir is in)
The file is a TSK_FS_FILE struct that has: meta (contains size, type, addr, atime, ctime, crtime etc.), name, fs_info (pointer to the file system the file is in)
'''
def extraction(directory, pPath, pPathName):
    ''' Uses recursion to find every file and directory in the image and stores the important ones
        directory      - The directory to look in
        pPath          - Store the path address
        pPathName      - Store the path name
    '''
    address = directory.info.addr
    pPath.append(address)
        
    for f in directory:
        fname = f.info.name.name
        #print 'File/Directory name is: ', fname
        
        #Dont want the directory entries "." (self), ".." (parent) recovered by the SleuthKit.
        if fname in ['.', '..']:
            continue
                    
        try: 
            fType = f.info.meta.type
            #print 'It is a ', fType    
        except:
            #print 'Error!Unable to retrieve the file type of ', fname
            continue
         
        # Try to store the full filepath by joining the parentPath and the filename
	outputPath ='./%s' % ('/'.join(pPathName))
	        
        '''   
        find out if the file is a directory
        pytsk3.TSK_FS_META_TYPE_REG  - Regular file
        pytsk3.TSK_FS_META_TYPE_DIR  - Directory file
        '''
        if fType == pytsk3.TSK_FS_META_TYPE_DIR:
            #found a directory, find all files in it
            subdirectory = f.as_directory()
            inode = subdirectory.info.addr
            pPathName.append(fname)
                     
      
            if inode not in pPath:
                extraction(subdirectory, pPath, pPathName)
                pPathName.pop(-1)

        '''
        Process file 
        '''
        if fType == pytsk3.TSK_FS_META_TYPE_REG:
            #print 'Defenitely a file: ', fname
                    
            #Extract File Information
            if fname == '$MFT':
                print '    Found Master File Table...Starting extraction process'
                outfile = open('files/MFT', 'w')
                filedata = f.read_random(0, f.info.meta.size)
                outfile.write(filedata)
                outfile.close()
                
            #Extract Windows Registry Information
            elif (fname == 'SAM' or fname == 'sam') and outputPath.endswith('config'):
                print '    Found SAM Hive in %s...Starting extraction process' % (outputPath)
                outfile = open('files/SAM', 'w')
                filedata = f.read_random(0, f.info.meta.size)
                outfile.write(filedata)
                outfile.close()
                
            elif (fname == 'SECURITY' or fname == 'security') and outputPath.endswith('config'):
                print '    Found SECURITY Hive in %s...Starting extraction process' % (outputPath)
                outfile = open('files/SECURITY', 'w')
                filedata = f.read_random(0, f.info.meta.size)
                outfile.write(filedata)
                outfile.close()
                
            elif (fname == 'SYSTEM' or fname == 'system') and outputPath.endswith('config'):
                print '    Found SYSTEM Hive in %s...Starting extraction process' % (outputPath)
                outfile = open('files/SYSTEM', 'w')
                filedata = f.read_random(0, f.info.meta.size)
                outfile.write(filedata)
                outfile.close()
                
            elif (fname == 'SOFTWARE' or fname == 'software') and outputPath.endswith('config'):
                print '    Found SOFTWARE Hive in %s...Starting extraction process' % (outputPath)
                outfile = open('files/SOFTWARE', 'w')
                filedata = f.read_random(0, f.info.meta.size)
                outfile.write(filedata)
                outfile.close()
                
            elif fname == 'NTUSER.DAT' and ('LocalService' not in outputPath) and ('NetworkService' not in outputPath):
                print '    Found NTUSER.DAT in %s ...Starting extraction process' % (outputPath)
                
                #Store file
                outfile = open('files/NTUSER.DAT', 'w')
                filedata = f.read_random(0, f.info.meta.size)
                outfile.write(filedata)
                outfile.close() 
                
                #Extract NTUSER.DAT information to .csv files, immediately because we might have more than one users
                substr = outputPath[outputPath.rfind('/')+1:]
                extractSystemInfo.extractNTUSERInfo(substr)
                    
    pPath.pop(-1)


def parseImage(diskPath):
    
    filenames = pyewf.glob(diskPath)
    ewf_handle = pyewf.handle()
    ewf_handle.open(filenames)

    #call class to parse .EO1 image with pytsk3
    img_Info = ewf_Img_Info(ewf_handle)

    try:
        partitionTable = pytsk3.Volume_Info(img_Info)
    
    except IOError:
        print "Error!Could not determine partition type ", filenames
        sys.exit(0)
        
    #find partitions
    for partition in partitionTable:
        print partition.addr, partition.desc, "%s   %s   (%s)" % (partition.start, partition.start * 512, partition.len)
    
        if 'NTFS' in partition.desc:
            fileSystemObject = pytsk3.FS_Info(img_Info, offset = (partition.start * 512))

            #Extract all files
            directory = fileSystemObject.open_dir(path = '/')
        
            #find all the files of the system
            extraction(directory, [], [])

    ewf_handle.close()
    

def main(): 
        
    diskPath = '/Volumes/Elements/York MSc Cyber Security (CYB)/FACI Exercises/Exercises/Forensic_1/Forensic_workshop_1.EO1'
    #diskPath = '/Volumes/Elements/York MSc Cyber Security (CYB)/FACI Exercises/Exercises/Assessment/Image/Money-transfer.EO1'
    #diskPath = '/Users/anastasioskoutlis/Developer/York MSc Cyber Security (CYB)/Cyber Security Individual Project (PCYB) /Scenarios/1/nps-2008-jean.E01'
    #diskPath = '/Users/anastasioskoutlis/Developer/York MSc Cyber Security (CYB)/Cyber Security Individual Project (PCYB)/Scenarios/3/Internet_Foreniscs_IE10_image.ad1'

    #Print partion information for every partition of the image given
    parseImage(diskPath)
    
    #Extract MFT information to .csv
    print 'Extracting MFT information to csv...'
    os.system('analyzeMFT.py -f forfiles/MFT -o forcsv/mft.csv')

    #Extract Registry information to .csv
    print 'Extracting Registry information to csv...'
    extractSystemInfo.systemInfo()
    extractSystemInfo.softwareInfo()
    extractSystemInfo.deviceInfo()


if __name__ == "__main__":
    main()