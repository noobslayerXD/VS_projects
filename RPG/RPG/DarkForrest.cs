using System;

namespace RPG
{
    public class DarkForrest
    {
        Battle ba = new Battle();

        //Hvis man prøver på at slå trolden
        public void PunchingGoblin()
        {
            //vælger at bruge mange Console.WriteLine Istedet for bare at bruge code interperlation og bruge /n
            Console.WriteLine("You miss");
            Console.WriteLine("Do you want to try again?");
            Console.WriteLine("a.yes");
            Console.WriteLine("b.no");
            //Bruger if else statements da det er nemmere end switch statements når de er så små
            if (Console.ReadLine() == "a")
            {
                PunchingGoblin();
            }
            else if (Console.ReadLine() == "b")
            {
                Console.WriteLine("What do you then want to do?");
                Console.WriteLine("a.stab him");
                Console.WriteLine("b.talk to him");
                if (Console.ReadLine() == "a")
                {
                    StabbingGoblin();
                }
                else if (Console.ReadLine() == "b")
                {
                    GoblinTalk();
                }
            }
        }
        
        //Hvis man prøver på at stikke trolden ned
        public void StabbingGoblin()
        {
            Console.WriteLine("You miss");
            Console.WriteLine("Do you want to try again?");
            Console.WriteLine("a.yes");
            Console.WriteLine("b.no");
            if (Console.ReadLine() == "a")
            {
                StabbingGoblin();
            }
            else if (Console.ReadLine() == "b")
            {
                Console.WriteLine("What do you then want to do?");
                Console.WriteLine("a.punch him");
                Console.WriteLine("b.talk to him");
                if (Console.ReadLine() == "a")
                {
                    PunchingGoblin();
                }
                else if (Console.ReadLine() == "b")
                {
                    GoblinTalk();
                }
            }
        }
        //Hvor man skal vælge hvordan man vil slås med trolden
        public void Fight()
        {
            Console.WriteLine("How do you want to kill the dancing goblin?");
            Console.WriteLine("a.Punch him, you have a 0% chance of hitting him");
            Console.WriteLine("b.Stab him, 0% of hitting him");
        }
        //introen hvor trolden står og danser
        public void Dance()
        {
            Console.WriteLine("What do you do now?");
            Console.WriteLine("a.Dance With the goblin");
            Console.WriteLine("b.Kill him");


            if (Console.ReadLine() == "a")
            {
                Console.WriteLine("You dance with the goblin for an hour, what do you want to do now?");
                Console.WriteLine("a.Keep dancing with him");
                Console.WriteLine("b.Talk to him");
                Console.WriteLine("c.Kill Him");
                if (Console.ReadLine() == "a")
                {
                    Console.WriteLine("You die of exhaustion");
                    Console.WriteLine("You Lose");
                }
                else if (Console.ReadLine() == "b")
                {
                    GoblinTalk();
                }
                else if (Console.ReadLine() == "c")
                {
                    Fight();
                }
            }
            else if (Console.ReadLine() == "b")
            {
                Fight();
            }
        }
        //Trolden der fortæller om blomsterhaven
        public void GoblinTalk()
        {
            Console.WriteLine($"The goblin finally stops dancing and says:I am a god, but you arent, you should visit the flower garden");
            Console.WriteLine("You walk back the the flower garden");
            ba.BattleIntro();
        }
    }
}