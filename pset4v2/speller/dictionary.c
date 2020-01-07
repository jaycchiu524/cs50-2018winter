// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

void freeNode(node *currentNode);
// Represents a trie
node *root;

unsigned int counter = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));

    //In case no memory is allocated
    if (root == NULL)
    {
        return false;
    }

    //Default false to is_word and NULL to next node
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        counter ++;
        node *ptr = root;

        for(int i = 0, length = strlen(word); i < length; i++)
        {

            int j;
            if(isalpha(word[i]))
            {
                j = tolower(word[i])-'a';
            }

            else
            {
                j = N - 1;
            }

            if(ptr->children[j] == NULL)
            {
                if(i == (length - 1))
                {
                    ptr->is_word = true;
                }

                else
                {
                    node *cursor = malloc(sizeof(node));

                    //initialize a new node-children for a-z,\'
                    for (int k = 0; k < N; k++)
                    {
                        cursor->children[k] = NULL;
                    }

                    cursor->is_word = false;
                    ptr->children[j] = cursor;
                    ptr = cursor;
                }

            }

            else
            {
                ptr = ptr->children[j];
            }

        }


    }
    // Close dictionary
    fclose(file);

    // Indicate success
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
    node *ptr = root;

    for(int i = 0, length = strlen(word); i < length; i++)
    {
        int j;

        //for a -z
        if(isalpha(word[i]))
        {
            j = tolower(word[i])-'a';
        }

        //for \'
        else
        {
            j = N - 1;
        }


        //check if it is the last character
        if (i == length - 1)
        {
            if(ptr->is_word != 0)
            {
                return true;
            }

            else
            {
                return false;
            }
        }

        else
        {
            if(ptr->children[j] == NULL)
            {
                return false;
            }

            else
            {
                ptr = ptr->children[j];
            }

        }
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool
unload(void)
{
    for (int i = 0; i < 27; i++)
    {
        if (root->children[i] != NULL)
            {
                freeNode(root->children[i]);
            }
    }
    free(root);
    return true;
}

void freeNode(node *currentNode)
{
    for (int i = 0; i < 27; i++)
    {
        if (currentNode->children[i] != NULL)
            {
                freeNode(currentNode->children[i]);
            }
    }
    free(currentNode);
}
