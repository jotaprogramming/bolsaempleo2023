const addTagBtn = document.getElementById("addTagBtn");

/**
 * The function removes a tag from a list and updates the corresponding input field.
 */
function removeTag() {
  const removeTagBtn = document.getElementsByName("removeTagBtn");
  removeTagBtn.forEach((element) => {
    element.addEventListener("click", () => {
      const tagList = document.getElementById("tagList");
      const tags = document.getElementById("id_tags");

      const ID = element.getAttribute("id");

      const tagElements = tagList.childNodes;
      tagElements.forEach((tagElement) => {
        if (tagElement.nodeName == "DIV") {
          const ID_PARENT = tagElement.getAttribute("id");

          if (ID_PARENT == ID) {
            const tagName = tagElement.querySelector(".tag").innerHTML;

            let tagArray = tags.value.split(",");

            tagList.removeChild(element);

            tagArray = tagArray.filter(
              (value) => value.toLowerCase() != tagName.toLowerCase()
            );

            const newValue = tagArray.join(",");
            tags.value = `${newValue}`;
          }
        }
      });
    });
  });
}

/* This code block adds an event listener to the HTML element with the ID "addTagBtn". When this button
is clicked, it retrieves the values of the input fields with the IDs "searchTag" and "id_tags". It
then checks if the value of "searchTag" is not empty and if the number of tags in "id_tags" is less
than 5. If these conditions are met, it converts the value of "searchTag" to lowercase and checks if
it already exists in the "id_tags" field. If it does not exist, it creates a new HTML element with
the tag value and appends it to the HTML element with the ID "tagList". It also updates the value of
the "id_tags" field with the new tag value. Finally, it calls the "removeTag()" function to add an
event listener to the newly created tag element to allow it to be removed. */
if (addTagBtn) {
  addTagBtn.addEventListener("click", () => {
    const searchTag = document.getElementById("searchTag");
    const tags = document.getElementById("id_tags");
    const tagList = document.getElementById("tagList");
    let tagValue = searchTag.value;

    if (tagValue) {
      let tagArray = tags.value ? tags.value.split(",") : [];
      if (tagArray.length < 5) {
        tagValue = tagValue.toLowerCase();

        let anyItem =
          tagArray && tagArray.some((value) => value.toLowerCase() == tagValue);

        if (!anyItem) {
          let div = document.createElement("div");
          div.classList.add("single__tag", "single__tag--remove");
          div.setAttribute("id", tagValue);
          div.setAttribute("name", "removeTagBtn");
          div.innerHTML = `
          <p class="tag text-lowercase m-0" style="min-height: 2rem">${tagValue}</p>
          `;

          tagArray =
            tagArray && tagArray.length > 0 && tagArray.filter((tag) => tag);

          tagArray = tagArray || [];

          tagArray.push(tagValue);
          const newValue = tagArray.join(",").replace(" ", "");
          tags.value = `${newValue}`;
          tagList.appendChild(div);
          removeTag();
        }
      }
      searchTag.value = "";
    }
  });
}
