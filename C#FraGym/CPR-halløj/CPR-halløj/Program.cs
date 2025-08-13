using System;

namespace CPR_halløj
{
    class Program
    {
        static void Main(string[] args)
        {
            int[] cpr = new int[10];
            string shit = Console.ReadLine();

            if (shit.Length < 10)
            {
                Console.WriteLine("Try again");
                return;
            }

            for (int i = 0; i < 10; i++)
            {
                cpr[i] = Convert.ToInt32(shit[i].ToString());
            }

            //ganger de forskellige tal med nogle tal
            int num1 = cpr[0] * 4;
            int num2 = cpr[1] * 3;
            int num3 = cpr[2] * 2;
            int num4 = cpr[3] * 7;
            int num5 = cpr[4] * 6;
            int num6 = cpr[5] * 5;
            int num7 = cpr[6] * 4;
            int num8 = cpr[7] * 3;
            int num9 = cpr[8] * 2;
            int num10 = cpr[9] * 1;

            //lægger tallene sammen
            int SumOfCpr = num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8 + num9 + num10;

            //ser om tallet går op i 11, og hvis det gør er det et rigtigt cpr-nummer og hvis ikke, så er det det falske sted
            if (SumOfCpr % 11 == 0)
            {
                Console.WriteLine("Det er et rigtigt cprnummer");
            }
            else
            {
                Console.WriteLine("DET ER DET FALSKE STED");
            }
        }
    }
}