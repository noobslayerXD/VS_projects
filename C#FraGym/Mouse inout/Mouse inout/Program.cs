using System;

namespace Mouse_inout
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            Head();
            int origRow;
            int origCol;

            void WriteAt(string s, int x, int y)
            {
                try
                {
                    Console.SetCursorPosition(origCol + x, origRow + y);
                    Console.Write(s);
                }
                catch (ArgumentOutOfRangeException e)
                {
                    Console.Clear();
                    Console.WriteLine(e.Message);
                }
            }

            void Head()
            {
                // Clear the screen, then save the top and left coordinates.
                Console.Clear();
                origRow = Console.CursorTop;
                origCol = Console.CursorLeft;

                // Draw the left side of a 5x5 rectangle, from top to bottom.
                WriteAt("+", 0, 0);
                WriteAt("|", 0, 1);
                WriteAt("|", 0, 2);
                WriteAt("|", 0, 3);
                WriteAt("|", 0, 4);
                WriteAt("|", 0, 5);
                WriteAt("|", 0, 6);
                WriteAt("|", 0, 7);
                WriteAt("|", 0, 8);
                WriteAt("|", 0, 9);
                WriteAt("|", 0, 10);
                WriteAt("|", 0, 11);
                WriteAt("|", 0, 12);
                WriteAt("|", 0, 13);
                WriteAt("|", 0, 14);
                WriteAt("|", 0, 15);
                WriteAt("|", 0, 16);
                WriteAt("|", 0, 17);
                WriteAt("|", 0, 18);
                WriteAt("|", 0, 19);
                WriteAt("|", 0, 20);
                WriteAt("|", 0, 21);
                WriteAt("|", 0, 22);
                WriteAt("|", 0, 23);
                WriteAt("|", 0, 24);
                WriteAt("|", 0, 25);
                WriteAt("|", 0, 26);
                WriteAt("|", 0, 27);
                WriteAt("|", 0, 28);
                WriteAt("+", 0, 29);

                // Draw the bottom side, from left to right.
                WriteAt("---------------------------------------------------------------------------------------------------------------------", 1, 29); // shortcut: WriteAt("---", 1, 4)
                WriteAt("+", 118, 29);

                // Draw the right side, from bottom to top.
                WriteAt("|", 118, 28);
                WriteAt("|", 118, 27);
                WriteAt("|", 118, 26);
                WriteAt("|", 118, 25);
                WriteAt("|", 118, 24);
                WriteAt("|", 118, 23);
                WriteAt("|", 118, 22);
                WriteAt("|", 118, 21);
                WriteAt("|", 118, 20);
                WriteAt("|", 118, 19);
                WriteAt("|", 118, 18);
                WriteAt("|", 118, 17);
                WriteAt("|", 118, 16);
                WriteAt("|", 118, 15);
                WriteAt("|", 118, 14);
                WriteAt("|", 118, 13);
                WriteAt("|", 118, 12);
                WriteAt("|", 118, 11);
                WriteAt("|", 118, 10);
                WriteAt("|", 118, 9);
                WriteAt("|", 118, 8);
                WriteAt("|", 118, 7);
                WriteAt("|", 118, 6);
                WriteAt("|", 118, 5);
                WriteAt("|", 118, 4);
                WriteAt("|", 118, 3);
                WriteAt("|", 118, 2);
                WriteAt("|", 118, 1);
                WriteAt("+", 118, 0);

                // Draw the top side, from right to left.
                WriteAt("---------------------------------------------------------------------------------------------------------------------", 1, 0); // ...

                WriteAt("All done!", 0, 31);
                Console.WriteLine();
            }
        }
    }

}
