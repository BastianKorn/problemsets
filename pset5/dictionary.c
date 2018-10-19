/**
 * Implements a dictionary's functionality using hashtable
 */

#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

//declare hashtable (array of pointers)
node *hashtable[SIZE]={NULL};

//declare dictionary words counter
unsigned int *ptr_counter;
unsigned int word_counter;


/**
*Returnes hash value.
* this hash function was found on the internet but there was no author mentioned
*/
 unsigned int hash_func(const char* word)
{
    unsigned int hash = 0;
    for (int i=0; word[i]!= '\0'; i++)
    {
        hash = 31*hash + word[i];
    }
    return hash % SIZE;
}



/**
 *Returns a new node
 */
struct node *getNewNode(const char* word)
{
    struct node *newNode=(struct node*)malloc(sizeof(struct node));
     if(newNode==NULL)
    {
        printf("Could not access memory\n");
        unload();
        return false;
    }
    newNode->next=NULL;
    strcpy(newNode->word, word);

    return newNode;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    //declares a string to hold a word converted to lowercase for hashing
    char tword[LENGTH+1];

    int n=strlen(word);

    for(int i=0; i<n+1; i++)
    {
        tword[i]=tolower(word[i]);
    }

    //creates a node pointer pointing to the first node in hashtable hash_func-th element
    node *cursor=hashtable[hash_func(tword)];

    //search for a word in a linked list linked to hashtable element
    while(cursor!=NULL)
    {
        if(strcasecmp(cursor->word, word)==0)
        {
            return true;
        }
        else
        {
            cursor=cursor->next;
        }
    }

    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // try to open dictionary to load
    FILE *fpd=fopen(dictionary, "r");
    if(fpd==NULL)
    {
        printf("Could not open %s\n.", dictionary);
        return false;
    }

    //initialize word counter to 0
    word_counter=0;

    //declare char array (word) to be read from dictionary
    char dword[47];

    //declare variable for hash value
    unsigned int hash=0;

    //scan dictionary word by word until the EOF is reached
    while(fscanf(fpd, "%s", dword)!=EOF)
    {
        hash=hash_func(dword);


        if(hashtable[hash]==NULL)
        {
            hashtable[hash]=getNewNode(dword);
            word_counter++;
        }
        else
        {
            node *newNode=getNewNode(dword);
            newNode->next=hashtable[hash];
            hashtable[hash]=newNode;
            word_counter++;
        }
    }

    //close dictionary
    fclose(fpd);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    ptr_counter=&word_counter;
    return word_counter;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for(int i=0; i<SIZE; i++)
    {
        node *cursor=hashtable[i];
        while(cursor!=NULL)
        {
            node *temp=cursor;
            cursor=cursor->next;
            free(temp);
        }
    }
    return true;
}
