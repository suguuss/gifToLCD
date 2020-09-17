/*---------------------------------------------------------------------------*-
   DrawOnScreen()
  -----------------------------------------------------------------------------
   Description : Displays a given image on a LCD
   Input       : array   : Array with the gif stored inside (gifToLCD.py) (2D Array)
               	 nbImage : Number of images in the gif
                 tempo   : Delay between every frame
   Output      : --
-*---------------------------------------------------------------------------*/
void DrawOnScreen(unsigned char array[][1024], unsigned char nbImage, unsigned char tempo)
{
	unsigned int x, y, i;

   	for (i = 0; i < nbImage; i++)
	{
		SelectPosLiCo(0,0);
		for(y = 0; y < 8; y++)
		{
			for (x = 0; x < 128; x++)
			{
				SelectPosLiCo(y,x);
				AfficherByte(array[i][x + 128*y]);
			}
		}
		
		Delay_1ms(tempo);
	}      
}

// Function is called inside the while loop 
while (1)
{
	DrawOnScreen(imgArray, NB_IMAGE, TEMPO_BOUCLE);
}
