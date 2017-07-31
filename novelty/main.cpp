//
//  main.cpp
//  NoveltyFilter
//
//  Created by Arend Hintze on 7/2/14.
//  Copyright (c) 2014 Arend Hintze. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include "singleBloomFilter.h"

using namespace std;

int main(int argc, const char * argv[]){
	vector<unsigned long long> primes;
	int charToKMap[256];
	unsigned char kMask;
	unsigned long long buffer,bufferMask;
	int intervall,intervallCounter=0;
	int intervallBuffer[2]={0,0};
	Filter *filter;
	int K;
	int N;
	FILE *ctkF;
	FILE *I,*O;
	int pos=0;
	for(int i=0;i<8;i++)
		printf("%i %s\n",i,argv[i+1]);
	primes.push_back((unsigned long long)atoi(argv[1]));
	K=atoi(argv[2]);
	N=atoi(argv[3]);
	kMask=(1<<K)-1;
	ctkF=fopen(argv[4],"r+t");
	buffer=(unsigned long long)0;
	bufferMask=((unsigned long long)1<<(unsigned long long)(N*K))-(unsigned long long)1;
	int d;
	
	for(int i=0;i<256;i++){
		fscanf(ctkF,"%i\n",&d);
		charToKMap[i]=d&kMask;
	}
	fclose(ctkF);
	filter=new Filter(primes[0]);
	I=fopen(argv[5],"r+t");
	O=fopen(argv[6],"w+t");
	filter->loadFilter(argv[7]);
	intervall=atoi(argv[8]);
	while(!feof(I)){
		char C;
		fscanf(I,"%c",&C);
		buffer=((buffer<<(unsigned long long)K)&bufferMask)+(unsigned long long)charToKMap[C];
		intervallBuffer[(int)filter->get(buffer)]++;
		filter->set(buffer);
		intervallCounter++;
		if(intervallCounter==intervall){
			fprintf(O,"%i,%i,%f\n",intervallBuffer[0],intervallBuffer[1],(float)intervallBuffer[0]/(float)intervall);
			intervallBuffer[0]=0;
			intervallBuffer[1]=0;
			intervallCounter=0;
		}
	}
	fclose(I);
	fclose(O);
	filter->saveFilter(argv[7]);
    return 0;
}

