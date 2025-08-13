using System;

namespace RPG
{

    public class Options
    {
        Battle ba = new Battle();
        DarkForrest d = new DarkForrest();
        public void ChooseAdventure()
        {
            Console.WriteLine("a.Into the dark forrest");
            Console.WriteLine("b.Go to the flower garden");
        }
        public void ChosenOption()
        {
            if (Console.ReadLine() == "a")
            {

                Console.WriteLine("You walk into the dark forrest and stumble upon a dancing dwarf");

                d.Dance();

            }
            else if (Console.ReadLine() == "b")
            {
                ba.BattleIntro();
            }
            else
            {
                Console.WriteLine("Type a or b you dumbass");
                Console.ReadLine();
            }
        }
    }
}