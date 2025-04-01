using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class TutorialManager : MonoBehaviour
{

    public TextMeshPro diagBox;
    public string linkText = "Linked";
    public string unlinkText = "Unlinked";
    public string relinkText = "Relinked";
    public string reunlinkText = "Reunlinked";

    private int dialog_trigger = 0;

    // Start is called before the first frame update
    void Start()
    {
        SingletonMaster.Instance.EventManager.LinkEvent.AddListener(OnLinked);
        SingletonMaster.Instance.EventManager.UnlinkEvent.AddListener(OnUnlinked);
    }

    private void OnLinked(GameObject obj, GameObject instigator)
    {
        if (diagBox == null)
            return;

        if (obj == gameObject && instigator.CompareTag("Player"))
        {
            if (dialog_trigger < 1)
            {
                diagBox.text = linkText; // Or whatever text you want
            }
            else
            {
                diagBox.text = relinkText;
            }
        }
    }

    private void OnUnlinked(GameObject obj, GameObject instigator)
    {
        if (diagBox == null)
            return;

        if (obj == gameObject && instigator.CompareTag("Player"))
        //obj.GetComponent<TextMeshPro>();
        {
            if (dialog_trigger < 1)
            {
                diagBox.text = unlinkText; // Or whatever text you want
                dialog_trigger = 1;
            }
            else
            {
                diagBox.text = reunlinkText;
            }
        }
    }
}
