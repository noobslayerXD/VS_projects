using System;
using System.Threading;

namespace RPGv3
{
    public class Story
    {
        public void ded()
        {
            //Console.Clear();
            Console.WriteLine("ded");
        }
        public void Intro()
        {
            //Console.Clear();

            Options op = new Options();
            Battle ba = new Battle();

            Console.WriteLine("Welcome Adventurer, where do you wanna go?");
            int op1 = op.Option1();

            if (op1 == 1) {
                Scene2();
            }
            else if (op1 == 2)
            {
                ba.battleFlowers();
                Console.WriteLine("You barely managed to escape and get back to where you were going!");
                Console.WriteLine("You lose 1 HP, and you now only have 3 left");
                Console.WriteLine("You walk into the dark forrest and stumble upon a dancing dwarf");
                Scene2();
            }
            else
            {
                Console.WriteLine("Please pick the options provided");
                Intro();
            }
        }
        public void Scene2()
        {
            //Console.Clear();

            Options op = new Options();
            Battle ba = new Battle();

            Console.WriteLine("What will you do now?");
            int op2 = op.Option2();

            if (op2 == 1)
            {
                ded();
            }
            else if (op2 == 2)
            {
                Scene2();
            }
            else if (op2 == 3)
            {
                int baDwarf = ba.battleDwarf();

                if (baDwarf == 505)
                {
                    ded();
                }

                if (baDwarf > 3 || baDwarf < 500)
                {
                    Scene3();
                }
            }
        }

        public void Scene3()
        {
            Console.WriteLine("You've found the gold, by pressing the wrong button!");
            Console.WriteLine("You're Winner!");
        }
    }
}