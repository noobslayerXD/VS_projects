using System;
using System.Threading;

namespace RPGv3
{
    public class Battle
    {
        public void battleFlowers()
        {
            Header head = new Header();
            head.flag = 1;
        }

        public int battleDwarf()
        {
            Random rng = new Random();
            int rand = rng.Next(1, 10);

            Header header = new Header();

            string baDwarfOption;

            Console.WriteLine("How will you attack the dwarf?");
            Console.WriteLine("a. Punch the dwarf!");
            Console.WriteLine("b. Stab the dwarf!");

            baDwarfOption = Console.ReadLine();

            if (header.flag == 1)
            {
                header.health = 3;
                header.result = 0;
                header.flag = 2;
            }
            else if (header.flag == 0)
            {
                header.health = 4;
                header.result = 0;
                header.flag = 2;
            }

            if (header.health <= 0)
            {
                return 505;
            }
            else if (header.result <= 5)
            {
                if (baDwarfOption == "a")
                {
                    if ((rand % 2) == 0)
                    {
                        Console.WriteLine("You hit the dwarf!");
                        Console.WriteLine("It loses 1 HP");
                        header.result++;
                        battleDwarf();
                    }
                    else
                    {
                        Console.WriteLine("You missed!");
                        Console.WriteLine("The dwarf attacks, and you lose 1 HP!");
                        header.health--;
                        battleDwarf();
                    }
                }
                else if (baDwarfOption == "b")
                {
                    if ((rand % 2) == 0)
                    {
                        Console.WriteLine("You missed!");
                        Console.WriteLine("The dwarf attacks, and you lose 1 HP!");
                        header.health--;
                        battleDwarf();
                    }
                    else
                    {
                        Console.WriteLine("You hit the dwarf!");
                        Console.WriteLine("It loses 1 HP");
                        header.result++;
                        battleDwarf();
                    }
                }

            }
            else
            {
                return header.result;
            }
            return 125435;

        }
    }
}
