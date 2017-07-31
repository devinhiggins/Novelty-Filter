//
//  singleBloomFilter.cpp
//  twitterFilter
//
//  Created by Arend on 12/6/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#include "singleBloomFilter.h"

Filter::Filter(unsigned long long thePrime){
    prime=thePrime;
    P=(unsigned char*)malloc(sizeof(unsigned char)*((prime>>(unsigned long long)3)+(unsigned long long)1));
    memset(P, 0, (prime>>(unsigned long long)3)+(unsigned long long)1);
    load=(unsigned long long) 0;
    
}
Filter::~Filter(){
    free(P);
}

void Filter::set(unsigned long long K){
    unsigned long long L=(K%prime)>>(unsigned long long)3;
    unsigned long long l=L&(unsigned long long)7;
    unsigned char a=(P[L]>>l)&1;
    if(a==0){
        load++;
        P[L]|=1<<l;
    }
//    printf("setK:%llu to:%llu\n",K,L);
}

unsigned char Filter::get(unsigned long long K){
    unsigned long long L=(K%prime)>>(unsigned long long)3;
    unsigned long long l=L&(unsigned long long)7;
    return (P[L]>>l)&1;
}

void Filter::saveFilter(const char *filename){
	FILE *F=fopen(filename,"w");
	fwrite(P, sizeof(unsigned char), ((prime>>(unsigned long long)3)+(unsigned long long)1), F);
	fclose(F);
}

void Filter::loadFilter(const char *filename){
	FILE *F=fopen(filename,"r");
	if(F==NULL)
		printf("No file to load from!\n");
	else{
		fread(P, sizeof(unsigned char), ((prime>>(unsigned long long)3)+(unsigned long long)1), F);
		fclose(F);
	}
}
