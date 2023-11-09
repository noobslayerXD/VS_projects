using System;

namespace RPG
{
    class Program
    {
        static void Main(string[] args)
        {
            Story jurney = new Story();
            Options j = new Options();
            DarkForrest d = new DarkForrest();

            jurney.Intro();
            j.ChooseAdventure();
            j.ChosenOption();
        }
    }
}
