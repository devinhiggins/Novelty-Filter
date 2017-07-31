//
//  singleBloomFilter.h
//  twitterFilter
//
//  Created by Arend on 12/6/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#ifndef twitterFilter_singleBloomFilter_h
#define twitterFilter_singleBloomFilter_h

using namespace std;

class Filter{
public:
    unsigned long long prime;
    unsigned char *P;
    unsigned long long load;
    Filter(unsigned long long thePrime);
    ~Filter();
    void set(unsigned long long K);
    unsigned char get(unsigned long long K);
	void saveFilter(const char *filename);
	void loadFilter(const char *filename);
};


#endif
