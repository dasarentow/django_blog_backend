#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define BUFFER_SIZE 1024

void run_custom_command(const char *custom_cmd);

/**
 * main - Entry point of the shell program.
 */
int main(void)
{
    char user_input[BUFFER_SIZE];

    while (1)
    {
        printf("$ ");
        fgets(user_input, BUFFER_SIZE, stdin);

        user_input[strlen(user_input) - 1] = '\0';

        if (strncmp(user_input, "exit", 4) == 0)
        {
            printf("Exiting the custom shell...\n");
            break;
        }

        run_custom_command(user_input);
    }

    return 0;
}

/**
 * Execute a given custom command.
 */
void run_custom_command(const char *custom_cmd)
{
    /* Check for the built-in exit command */
    if (strncmp(custom_cmd, "exit", 4) == 0)
    {
        int status = 0;

        if (strlen(custom_cmd) > 4)
        {
            char status_str[BUFFER_SIZE];
            strncpy(status_str, custom_cmd + 4, BUFFER_SIZE - 1);
            status_str[BUFFER_SIZE - 1] = '\0';
            status = atoi(status_str);
        }
        exit(status);
    }

    pid_t pid = fork();

    if (pid == -1)
    {
        perror("Fork failed");
        return;
    }
    else if (pid == 0)
    {
        char cmd_copy[BUFFER_SIZE];
        strcpy(cmd_copy, custom_cmd);

        char *token;
        char *cmd_args[64];
        int i = 0;

        while ((token = strtok(i == 0 ? cmd_copy : NULL, " ")))
        {
            cmd_args[i++] = token;
        }

        cmd_args[i] = NULL;

        for (int j = 0; cmd_args[j] != NULL; j++)
        {
            if (cmd_args[j][0] == '$')
            {
                char *env_var = getenv(cmd_args[j] + 1);
                if (env_var != NULL)
                {
                    cmd_args[j] = env_var;
                }
            }
        }

        if (execvp(cmd_args[0], cmd_args) == -1)
        {
            perror("Custom command execution failed");
            exit(EXIT_FAILURE);
        }
    }
    else
    {
        int status;
        waitpid(pid, &status, 0);
    }
}

// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>
// #include <sys/types.h>
// #include <sys/wait.h>
// #include <unistd.h>

// #define BUFFER_SIZE 1024

// void run_custom_command(const char *custom_cmd);

// /**
//  * main - Entry point of the shell program.
//  */
// int main(void)
// {
//     char user_input[BUFFER_SIZE];

//     while (1)
//     {
//         printf("$ ");
//         fgets(user_input, BUFFER_SIZE, stdin);

//         user_input[strlen(user_input) - 1] = '\0';

//         if (strcmp(user_input, "exit") == 0)
//         {
//             printf("Exiting the custom shell...\n");
//             break;
//         }

//         run_custom_command(user_input);
//     }

//     return 0;
// }

// /**
//  * Execute a given custom command.
//  */
// void run_custom_command(const char *custom_cmd)
// {
//     pid_t pid = fork();

//     if (pid == -1)
//     {
//         perror("Fork failed");
//         return;
//     }
//     else if (pid == 0)
//     {
//         char cmd_copy[BUFFER_SIZE];
//         strcpy(cmd_copy, custom_cmd);

//         // Tokenize the command
//         char *token;
//         char *cmd_args[64];
//         int i = 0;

//         while ((token = strtok(i == 0 ? cmd_copy : NULL, " ")))
//         {
//             cmd_args[i++] = token;
//         }

//         cmd_args[i] = NULL;

//         // Handle environment variable expansion
//         for (int j = 0; cmd_args[j] != NULL; j++)
//         {
//             if (cmd_args[j][0] == '$')
//             {
//                 char *env_var = getenv(cmd_args[j] + 1);
//                 if (env_var != NULL)
//                 {
//                     cmd_args[j] = env_var;
//                 }
//             }
//         }

//         if (execvp(cmd_args[0], cmd_args) == -1)
//         {
//             perror("Custom command execution failed");
//             exit(EXIT_FAILURE);
//         }
//     }
//     else
//     {
//         int status;
//         waitpid(pid, &status, 0);
//     }
// }
