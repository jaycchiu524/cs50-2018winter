// Implements a dictionary's functionality
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

int counter = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table, TODO
    while (fscanf(file, "%s", word) != EOF)
    {
         // let n be 0-25, 0 = a, 1 =b ...
        int n = hash(word);

        node *tmp = malloc(sizeof(node));
        strcpy(tmp->word, word);
        tmp->next = NULL;


        if (hashtable[n])
        {
            for(node *ptr = hashtable[n]; ptr != NULL; ptr = ptr->next)
            {
                if(ptr->next == NULL)
                {
                    ptr->next = tmp;
                    counter++;
                    break;
                }
            }
        }

        else
        {
            hashtable[n] = tmp;
            counter++;
        }


    }

    // Close dictionary
    fclose(file);
    return true;

}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}


// Returns true if word is in dictionary else false
bool check(const char *word)
{

    char tmp[LENGTH+1];

    tmp[strlen(word)]='\0';

    for(int i = 0, j = strlen(word); i < j; i++)
    {
        tmp[i] = tolower(word[i]);
    }

    int n = hash(word);
    node *checker = hashtable[n];

    if (checker == NULL)
    {
        return false;
    }

    else
    {

        while (checker != NULL)
        {
            if (strcmp(checker->word, tmp) == 0)
            {
                return true;
            }

            else
            {
                checker = checker->next;
            }

        }

        return false;
    }



}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    node *cursor;

    for(int i = 0; i < N; i++)
    {
        cursor = hashtable[i];

        while(cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }

    }
    free(cursor);
    return true;
}
