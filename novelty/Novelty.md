

```python
from run_novelty import Novelty
n = Novelty()
n.get_novelty("/Users/devinhiggins/Projects/novelty/texts/modernism/James_TheAmbassadors.txt")
n.graph_novelty()
```

    Text                                               Slope      r^2        # Intervals Lexical Diversity
    James_TheAmbassadors.txt                           -0.0024    0.903      86         0.0694404961881



<iframe id="igraph" scrolling="no" style="border:none;"seamless="seamless" src="https://plot.ly/~msunovelty/34" height="525" width="100%"></iframe>



```python
from run_novelty import Novelty
n = Novelty()
n.get_novelty("/Users/devinhiggins/Projects/novelty/texts/victorian/Stevenson_JekyllandHyde.txt")
n.graph_novelty()
```

    Text                                               Slope      r^2        # Intervals
    Stevenson_JekyllandHyde.txt                        -0.0042    0.5621     13        



<iframe id="igraph" scrolling="no" style="border:none;"seamless="seamless" src="https://plot.ly/~msunovelty/32" height="525" width="100%"></iframe>


### Modernist


```python
from run_novelty import Novelty
n = Novelty()
n.corpus_novelty("/Users/devinhiggins/Projects/novelty/texts/modernism/")
```

    Text                                               Slope      r^2        # Intervals Lexical Diversity
    James_TurnoftheScrew.txt                           -0.005     0.9356     22         0.117867121277
    Ford_ParadesEnd.txt                                -0.0019    0.8491     112        0.0911575950961
    Ford_TheGoodSoldier.txt                            -0.0044    0.8971     41         0.100595728837
    Pound_Personae.txt                                 -0.0009    0.003      5          0.273397364306
    Conrad_HeartofDarkness.txt                         -0.0056    0.9208     21         0.158940397351
    Forster_HowardsEnd.txt                             -0.0023    0.9168     61         0.0932527638283
    Joyce_Dubliners.txt                                -0.0047    0.8229     36         0.111886661035
    Joyce_Ulysses.txt                                  -0.0008    0.593      151        0.114623476525
    Faulkner_ARoseForEmily.txt                         -0.0359    1.0        2          0.292808683853
    Woolf_ToTheLighthouse.txt                          -0.0048    0.771      38         0.103628363269
    Fitzgerald_TheGreatGatsby.txt                      -0.0049    0.942      26         0.129862047505
    Fitzgerald_TenderIsTheNight.txt                    -0.0025    0.8795     61         0.1121436505
    Eliot_WasteLand.txt                                -0.0489    1.0        2          0.413024850043
    West_ReturnOfTheSoldier.txt                        -0.0047    0.9013     16         0.156494894324
    Joyce_PortraitofanArtist.txt                       -0.0014    0.3085     46         0.111827982355
    Forster_RoomWithAView.txt                          -0.0032    0.9099     37         0.111791615253
    Stein_TenderButtons.txt                            -0.016     0.5281     7          0.174610602313
    Lawrence_LadyChatterleysLover.txt                  -0.0027    0.8141     64         0.0809855245741
    Stein_AutobiographyofAliceBToklas.txt              -0.0039    0.8553     50         0.0733217172974
    Richardson_PointedRoofs.txt                        -0.0052    0.8698     32         

    /Library/Python/2.7/site-packages/scipy/stats/stats.py:3020: RuntimeWarning:
    
    invalid value encountered in double_scalars
    
    /Library/Python/2.7/site-packages/scipy/stats/stats.py:3016: RuntimeWarning:
    
    invalid value encountered in sqrt
    


    0.132261092458
    Eliot_TheWasteLand.txt                             nan        0.0        1          0.390526664458
    Woolf_MrsDalloway.txt                              -0.0044    0.8083     35         0.120332670517
    Woolf_JacobsRoom.txt                               -0.0028    0.8254     31         0.145737771091
    Faulkner_TheSoundAndTheFury.txt                    -0.0011    0.0944     50         0.0658634953464
    Wharton_HouseOfMirth.txt                           -0.003     0.9014     73         0.0922509796633
    Conrad_SecretAgent.txt                             -0.0033    0.823      52         0.113885559551
    DosPassos_ThreeSoldiers.txt                        -0.0021    0.7176     74         0.0729719229562
    James_TheAmbassadors.txt                           -0.0024    0.903      86         0.0694404961881
    Stein_ThreeLives.txt                               -0.0064    0.7219     44         0.0388725000581


    /Library/Python/2.7/site-packages/scipy/stats/stats.py:3018: RuntimeWarning:
    
    invalid value encountered in double_scalars
    


### Victorian


```python
from run_novelty import Novelty
n = Novelty()
n.corpus_novelty("/Users/devinhiggins/Projects/novelty/texts/victorian/")
```

    Text                                               Slope      r^2        # Intervals Lexical Diversity
    Austen_PrideandPrejudice.txt                       -0.0035    0.8336     68         0.0560067737533
    Gissing_NewGrubStreet.txt                          -0.002     0.8586     102        0.0589740550791
    Eliot_SilasMarner.txt                              -0.0039    0.8693     39         0.108434413874
    Dickens_GreatExpectations.txt                      -0.002     0.8351     99         0.0668185269552
    Conrad_HeartofDarkness.txt                         -0.0056    0.9215     21         0.158940397351
    Austen_Emma.txt                                    -0.0027    0.868      88         0.0632186825739
    Hardy_JudetheObscure.txt                           -0.002     0.8954     80         0.0857782007906
    Hardy_TessoftheD'Urbervilles.txt                   -0.0022    0.9167     83         0.0919617611418
    Gissing_OddWomen.txt                               -0.0025    0.903      77         0.0709811050196
    Gaskell_MaryBarton.txt                             -0.002     0.9366     87         0.0680359594679
    Wilde_ImportanceofbeingEarnest.txt                 -0.0155    0.9107     11         0.130205536298
    Stevenson_JekyllandHyde.txt                        -0.0042    0.5621     13         0.161597697573
    Thackeray_VanityFair.txt                           -0.0014    0.8652     170        0.0625325655875
    Gaskell_NorthAndsouth.txt                          -0.0019    0.8503     99         0.0661614352247
    Collins_WomaninWhite.txt                           -0.002     0.8118     135        0.0519629682614
    Collins_Moonstone.txt                              -0.0023    0.8177     105        0.0553201873254
    Flaubert_MadameBovary.txt                          -0.0028    0.9234     65         0.0948090243249
    Browning_AuroraLeigh.txt                           -0.0018    0.8028     48         0.121728234639
    Scott_Waverly.txt                                  -0.0018    0.8393     110        0.0856671286647
    Bronte_WutheringHeights.txt                        -0.0024    0.9457     64         0.0872966585589
    Wilde_PictureofDorianGrey.txt                      -0.0042    0.7769     42         0.0927443991853
    Trollope_BarchesterTowers.txt                      -0.0023    0.7942     109        0.0596583734861
    Stoker_Dracula.txt                                 -0.002     0.848      84         0.0654924600171
    Eliot_Middlemarch.txt                              -0.0016    0.8904     178        0.0579827673594
    Bronte_JaneEyre.txt                                -0.0013    0.8433     102        0.0799926343952
    Dickens_BleakHouse.txt                             -0.0013    0.8467     193        0.0505957446809
    Austen_MansfieldPark.txt                           -0.0028    0.8698     88         0.0526787168214
    Browning_MenandWomen.txt                           -0.0014    0.5493     20         0.195194188321
    Carlyle_PastandPresent.txt                         -0.0024    0.5318     62         0.119583135955
    Trollope_TheWayWeLiveNow.txt                       -0.0017    0.8332     190        0.0410642088673
    Braddon_LadyAudleysSecret.txt                      -0.0025    0.8381     82         0.0756925820594
    Eliot_DanielDeronda.txt                            -0.0013    0.7949     174        0.058254879672
    Schreiner_StoryofanAfricanFarm.txt                 -0.0023    0.6795     54         0.076379247531


### Realism


```python
from run_novelty import Novelty
n = Novelty()
n.corpus_novelty("/Users/devinhiggins/Projects/novelty/texts/Realism/")
```

    Text                                               Slope      r^2        # Intervals Lexical Diversity
    Wharton_CustomoftheCountry.txt                     -0.0023    0.9073     78         0.0887808741989
    Howells_ConfessionsStAugustine.txt                 -0.0071    0.7568     6          0.250760150241
    James_TurnoftheScrew copy.txt                      -0.005     0.9356     22         0.117867121277
    Crane_MaggieGirlOfTheStreets.txt                   -0.008     0.4886     13         0.188560708521
    Norris_McTeague.txt                                -0.0026    0.7337     63         0.0861350695956
    Alger_RaggedDick.txt                               -0.0054    0.7974     26         0.0995400376333
    Dreiser_TheGenius.txt                              -0.0014    0.7869     168        0.0521153997948
    Wharton_AgeofInnocence.txt                         -0.0028    0.8732     58         0.1013916894
    Davis_LifeintheIronMills.txt                       -0.0076    0.9623     8          0.207877015169
    Howells_SilasLapham.txt                            -0.003     0.8539     69         0.0690172951693
    Dunbar_TheUncalled.txt                             -0.0033    0.6974     27         0.117508464173
    Alger_TelegraphBoy.txt                             -0.0054    0.7365     20         0.103478283801
    Twain_TomSawyer.txt                                -0.0031    0.8898     38         0.116145848251
    Chesnutt_MarrowofTradition.txt                     -0.003     0.8532     50         0.102455183604
    Chopin_TheAwakening.txt                            -0.0044    0.8714     28         0.121277965556
    Wharton_EthanFrome.txt                             -0.0071    0.9575     18         0.136097743711
    London_CallOfTheWild.txt                           -0.005     0.8556     17         0.153151167915
    Sinclair_KingCoal.txt                              -0.0026    0.7988     67         0.0779251734228
    Twain_HuckFinn.txt                                 -0.003     0.8843     56         0.066123213101
    London_SeaWitch.txt                                -0.0027    0.8994     58         0.101499521631
    Dreiser_SisterCarrie.txt                           -0.0023    0.7692     87         0.0679686298631
    Wharton_HouseOfMirth copy.txt                      -0.003     0.9013     73         0.0922509796633
    Sinclair_TheJungle.txt                             -0.002     0.6632     80         0.077557534467
    Crane_RedBadgeOfCourage.txt                        -0.0048    0.8636     26         0.138264852076
    James_TheAmbassadors copy.txt                      -0.0024    0.903      86         0.0694404961881
    London_MartinEden.txt                              -0.0022    0.8718     77         0.0864919006168
    Norris_TheOctopus.txt                              -0.0015    0.7762     111        0.0735761514956



```python
with open("/Users/devinhiggins/Projects/novelty/texts/modernism/James_TheAmbassadors.txt") as f:
    data = f.read()
len(data) / 10000
```




    86




```python

```
