using System;
using System.Threading;

namespace RPGv3
{
    class Options
    {
        public void optionStart()
        {
            Story st = new Story();
        }

        public int Option1()
        {
            Console.WriteLine("a.Into the dark forest");
            Console.WriteLine("b.Go to the flower garden");
            int an1 = Answer1();
            return an1;
        }

        public int Answer1()
        {
            string read1 = Console.ReadLine();
            int flag1 = 0;

            if (read1 == "a")
            {
                Console.WriteLine("You walk into the dark forrest and stumble upon a dancing dwarf");
                flag1 = 1;
            }
            else if (read1 == "b")
            {
                Console.WriteLine("The flower garden is on fire, and a war is raging");
                flag1 = 2;
            }
            return flag1;
        }

        public int Option2()
        {
            Console.WriteLine("a. Dance with the dwarf");
            Console.WriteLine("b. Talk to the dwarf");
            Console.WriteLine("c. Kill the dwarf");
            int an2 = Answer2();
            return an2;
        }

        public int Answer2()
        {
            int flag2 = 0;
            string read2 = Console.ReadLine();

            if (read2 == "a")
            {
                Console.WriteLine("You begin to dance along with the dwarf");
                Console.WriteLine("The dwarf and you dance for a long time... in fact...");
                Console.WriteLine("You don't feel as though you're able to stop again");
                Console.WriteLine("You dance yourself to exhaustion, and then die");
                flag2 = 1;
            }
            else if (read2 == "b")
            {
                Console.WriteLine("You try to talk to the dwarf, but it doesn't seem to care");
                flag2 = 2;
            }
            else if (read2 == "c")
            {
                Console.WriteLine("You are now battling the dwarf!");
                flag2 = 3;
            }
            return flag2;
        }
    }
}