int i = 0;

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    for (i = 0; i < 255; i++)
    {
        Serial.println(i);
        delay(10);
    }
    i = 0;
}
