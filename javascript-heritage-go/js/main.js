
// Conversion table from ISO 639 alpha-2 codes (ISO 639-1:2002) to
// equivalent ISO 639-3 alpha-3 codes (ISO 639-3:2007).
const ISO_639_ALPHA2_CODE_TO_ISO_639_ALPHA3_CODE_MAPPING = {
    en: "eng",
    fr: "fra",
    vi: "vie",
    ch: "cha",
    it: "ita",

};

const LANGUAGE = {
    eng: "ENGLISH",
    fra: "FRANÇAIS",
    vie: "TIẾNG VIỆT",
    cha: "中文",
    ita: "ITALIANO"
};

// Declare variable
let scrolling = false;

// ======================================================================
// Display a List of Photos when Loading the Page
/**
 * Rendering photos
 */
async function loadPhotos(index) {
    let img;
    // Get the template element
    photos = await mHeritageGoService.getPhotos({
        limit: 2,
        offset: index
    });
    if ('content' in document.createElement('template')) {
        scrolling = false;
        for (i = 0; i < photos.length; i++) {
            const getPhotoPostTemplate = () => document.querySelector('#photoPostTemplate');
            const template = getPhotoPostTemplate();
            const fragment = template.content.cloneNode(true);
            const item = fragment.querySelector(".main__layout");

            // Get each image object
            img = await mHeritageGoService.getPhoto(photos[i], { includeSocialInfo: true });
            console.log(img);
            // Change content
            changeContentElement(item, img);

            // Append the new node:
            document.querySelector(".main").appendChild(item);
        }
    }
}
// =========================================================
/**
 * Change text content of each NodeList (template)
 *
 * @param item (required): a NodeList which is cloned from template
 *
 * @param img (required):  If the request passed, `img` a JavaScript
 * object which contains information of the photo
 */
function changeContentElement(item, img) {

    // Change the avatar of the header
    item.querySelector(".main__layout__header__avatar").src =
        `${img.account.picture_url}?size=thumbnail`;

    // Change the caption of the header
    item.querySelector(".main__layout__header__info__caption--title"
    ).textContent = img.title[0].content;

    // Change the location of the photo
    item.querySelector(
        ".main__layout__header__info__location--area__text"
    ).textContent = " " + img.area_name;

    // Change the date to take the phop
    let time = img.capture_time;
    let elem = item.querySelector(".main__layout__header__info__location--date");
    // In case capture time is undefined
    if (typeof time === "undefined") {
        elem.style.display = 'none'
    } else {
        item.querySelector(
            ".main__layout__header__info__location--date__text"
        ).textContent = " " + time;
    }

    // Change the source of the photo
    const image_url = img.image_url;
    item.querySelector(
        ".main__layout__photo"
    ).src = `${image_url}?size=medium`;

    // Change the like count of the header
    item.querySelector("#like-count").textContent = ` ${img.social.view_count}`;

    // Change the comment count of the header
    item.querySelector("#comment-count").textContent = ` ${img.social.comment_count}`;

    insertDropdownElement(item);

    let photoId = img.photo_id

    // Submits the user's translation for the selected language
    submitTranslatedCaption(item, photoId);

}


// =========================================================
/** WP19-20
 *  Submit the user's translation for the selected language
 *
 * @param item (required): a NodeList which is cloned from template
 *
 * @param photoId (required): the identification of the photograph
 */
function submitTranslatedCaption(item, photoId) {
    //get the editable element
    let editedElem = item.querySelector(".main__layout__header__info__caption--title")
    // let localeElem = item.querySelectorAll(".dropdown-item")
    let localeElem = item.querySelectorAll(".dropdown-item")

    // Allow the user to submit all the language
    for (i = 0; i < localeElem.length; i++) {
        let choosenLangElement = localeElem[i]
        choosenLangElement.addEventListener('click', function () {
            // Prevent to jump on the top of the page
            event.preventDefault();
            // Set addtribute of the caption so that the user can edit the content
            editedElem.setAttribute("contenteditable", "true")
            // Add event `Enter`and save the new caption by their language
            editedElem.addEventListener("keypress", function (evt) {
                let translatedVersion = editedElem.innerHTML;
                if (translatedVersion.length >= 0 && evt.keyCode === 13) {
                    localStorage.userEdits = translatedVersion;
                    // the suggested translation of the caption
                    let caption = translatedVersion;
                    // the language this translation is written in
                    let locale = choosenLangElement.id;
                    console.log("caption", translatedVersion)
                    console.log("photoID", photoId);
                    console.log("locale", locale);
                    // Calls the RESTful API to submits the user's translation for the selected language
                    mHeritageGoService
                        .suggestPhotoCaption(photoId, caption, locale)
                        .catch(error => {
                            console.log(error);
                        });
                    console.log("keypress is working");
                };
            });
        })
    }
}


// =========================================================
/**
 * Insert a dropdown available language list
 *
 * @param item (required): a NodeList which is cloned from template
 *
 */
function insertDropdownElement(item) {
    let block = item.querySelector(".dropdown-menu");
    // Get a list of languages of user
    let userLangList = getUserLangList();
    console.log("userLangList", userLangList);

    for (i = 0; i < userLangList.length; i++) {
        // The language as ISO 639-3 alpha-3 code
        let lang = userLangList[i]
        block.insertAdjacentHTML("beforeend", `<div class="dropdown-item" type="radio" id=${lang}><img id="translated-language-img" src="./img/flag/${lang}.png" alf="${lang}"><span id="translated-language-text">${LANGUAGE[lang]}</span></div>`)
    }
}


// =========================================================
/**
 *  Get a list of languages of user
 */
function getUserLangList() {
    // Get the preferred languages of the user are available
    let userLangList = navigator.languages || navigator.userLanguages;
    // Convert to a ISO 639-3 alpha-3 code
    let arr = Object.entries(ISO_639_ALPHA2_CODE_TO_ISO_639_ALPHA3_CODE_MAPPING);
    let converedList = [];
    for (let [key, value] of arr) {
        if (userLangList.includes(key)) {
            converedList.push(value);
        }
    };
    return converedList;
};


// Run ===================================================================
$(document).ready(function () {
    let index = 1;
    loadPhotos(index);
    scrolling = false;
    let $window = $(window);
    let window_height = $window.height();
    $window.scroll(function () {
        if (!scrolling) {
            if (
                //check to see if this current container is within viewport
                $window.scrollTop() // window top position
                >= $(document).height() - window_height - 2000
            ) {
                scrolling = true;
                index += 2;
                loadPhotos(index);
            }
        }
    });

    // ===========================================================
    // Edit Login Button Style
    $(".email-pass-input").each(function () {
        $(this).on("blur", function () {
            if (
                $(this)
                    .val()
                    .trim() != ""
            ) {
                $(this).addClass("has-val");
            } else {
                $(this).removeClass("has-val");
            }
        });
    });
    // ===========================================================
    // Show pass
    let showPass = 0;
    $(".btn-show-pass").on("click", function () {
        if (showPass == 0) {
            $(this)
                .next("input")
                .attr("type", "text");
            $(this)
                .find("i")
                .removeClass("fa fa-lock");
            $(this)
                .find("i")
                .addClass("fa fa-unlock");
            showPass = 1;
        } else {
            $(this)
                .next("input")
                .attr("type", "password");
            $(this)
                .find("i")
                .removeClass("fa fa-unlock");
            $(this)
                .find("i")
                .addClass("fa fa-lock");
            showPass = 0;
        }
    });


})


