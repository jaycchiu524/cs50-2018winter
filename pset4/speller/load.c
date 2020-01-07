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

unsigned int counter = 0;

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

        free(tmp);

    }

    // Close dictionary
    fclose(file);

    return true;

}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    printf("Word counts in dict: %i\n", counter);
    return counter;
}


int main (int argc, char *argv[])
{
    char *dictionary = argv[1];

    load(dictionary);
    size();

    return 0;
}