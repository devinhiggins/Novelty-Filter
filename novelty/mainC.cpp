//
//  main.cpp
//  CompareFilters
//
//  Created by Arend Hintze on 11/16/16.
//  Copyright © 2016 Arend Hintze. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
using namespace std;

int main(int argc, const char * argv[]) {
    int count[4]={0,0,0,0};
    if(argc<3){
        printf("not enough arguments!\n");
        exit(0);
    }
    ifstream fileA (argv[1], ios::in|ios::binary|ios::ate);
    ifstream fileB (argv[2], ios::in|ios::binary|ios::ate);
//    ifstream fileA ("A.txt", ios::in|ios::binary|ios::ate);
//    ifstream fileB ("B.txt", ios::in|ios::binary|ios::ate);
    int sizeA=(int)fileA.tellg();
    int sizeB=(int)fileB.tellg();
    //printf("File sizes: %i %i\n",sizeA,sizeB);
    if(sizeA!=sizeB){
        printf("different file sizes!\n");
    } else {
        char *memblockA = new char [sizeA];
        char *memblockB = new char [sizeB];
        char *memblockC = NULL;
        if(argc==4)
            memblockC=new char[sizeA];
//        printf("%p %p\n",memblockA,memblockB);
        fileA.seekg (0, ios::beg);
        fileB.seekg (0, ios::beg);
        fileA.read (memblockA, sizeA);
        fileB.read (memblockB, sizeB);
//        printf("loaded both files!\n");
        for(int i=0;i<sizeA;i++){
            int a=0;
            for(int j=0;j<8;j++){
                a=(((unsigned char)memblockA[i]>>j)&1)+((((unsigned char)memblockB[i]>>j)&1)*2);
                count[a]++;
            }
            if(memblockC!=NULL){
                memblockC[i]=memblockA[i]|memblockB[i];
            }
        }
        delete[] memblockA;
        delete[] memblockB;
        printf("%i %i %i %i\n",count[0],count[1],count[2],count[3]);
        if(memblockC!=NULL){
            ofstream fileC (argv[3], ios::out|ios::binary);
            fileC.write(memblockC,sizeA);
            fileC.close();
            
        }
    }
    fileB.close();
    fileB.close();
    return 0;
}
